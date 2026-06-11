import asyncio
from pathlib import Path

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph
from langgraph.prebuilt.chat_agent_executor import AgentState

from app.agents.tools import load_all_tools
from app.utils.constants import MODEL_NAME, PROMPTS_DIR


_agents_cache: dict[str, object] = {}
_init_locks: dict[str, asyncio.Lock] = {}
_memory = MemorySaver()


def _create_graph(model, tools, system_prompt):
    model_with_tools = model.bind_tools(tools)

    def chatbot(state: AgentState):
        messages = state["messages"]
        if system_prompt and (not messages or messages[0].type != "system"):
            from langchain_core.messages import SystemMessage
            messages = [SystemMessage(content=system_prompt)] + list(messages)
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    builder = StateGraph(AgentState)
    builder.add_node("agent", chatbot)
    builder.add_node("tools", ToolNode(tools, handle_tool_errors=True))
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")
    builder.set_entry_point("agent")
    return builder.compile(checkpointer=_memory)


def _get_init_lock(locale: str) -> asyncio.Lock:
    if locale not in _init_locks:
        _init_locks[locale] = asyncio.Lock()
    return _init_locks[locale]


async def create_agent_locale(locale: str):
    if locale in _agents_cache:
        return _agents_cache[locale]

    async with _get_init_lock(locale):
        if locale in _agents_cache:
            return _agents_cache[locale]

        prompt_path = Path(f"{PROMPTS_DIR}/{locale}.txt")

        if not prompt_path.exists():
            raise FileNotFoundError(
                f"System prompt not found for locale '{locale}'"
            )

        try:
            system_prompt = prompt_path.read_text(encoding="utf-8")
        except OSError as e:
            raise RuntimeError(f"Failed to read system prompt for locale '{locale}': {e}")

        if not system_prompt.strip():
            raise ValueError(f"System prompt for locale '{locale}' is empty")

        try:
            model = ChatOpenAI(model=MODEL_NAME)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize OpenAI model '{MODEL_NAME}': {e}")

        try:
            agent_tools = await load_all_tools(locale)
        except Exception as e:
            raise RuntimeError(f"Fallo al cargar herramientas: {e}")

        agent = _create_graph(model, agent_tools, system_prompt)
        _agents_cache[locale] = agent
        return agent
