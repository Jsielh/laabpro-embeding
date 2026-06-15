from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.interceptors import MCPToolCallRequest

from app.rag.vector_store import vector_stores, LANGUAGES
from app.utils.constants import MAX_RETRIEVED_DOCS
from app.core.settings import settings


def make_retrieve_context(locale: str):
    @tool(response_format="content_and_artifact")
    def retrieve_context(query: str) -> tuple[str, list]:
        """Retrieves relevant documents from the vector store based on the query."""
        retrieved_docs = vector_stores[locale].similarity_search(query, k=MAX_RETRIEVED_DOCS)

        serialized = "\n\n".join(
            f"Source: {doc.metadata}\nContent: {doc.page_content}"
            for doc in retrieved_docs
        )
        return serialized, retrieved_docs

    return retrieve_context


async def inject_org_id(request: MCPToolCallRequest, handler):
    if request.name.startswith("ZohoDesk_") and settings.ZOHO_DESK_ORG_ID is not None:
        query_params = {**request.args.get("query_params", {}), "orgId": int(settings.ZOHO_DESK_ORG_ID)}
        args = {**request.args, "query_params": query_params}

        if request.name == "ZohoDesk_createTicket" and settings.ZOHO_DESK_DEPARTMENT_ID is not None:
            body = request.args.get("body", {})
            body.pop("contactId", None)
            body.pop("departmentId", None)
            body = {"departmentId": int(settings.ZOHO_DESK_DEPARTMENT_ID), **body}
            args["body"] = body

        request = request.override(args=args)
    return await handler(request)


async def load_zoho_tools():
    if not settings.ZOHO_MCP_SERVER_URL:
        return []
    client = MultiServerMCPClient(
        {
            "zoho_desk": {
                "transport": "http",
                "url": settings.ZOHO_MCP_SERVER_URL,
            }
        },
        tool_interceptors=[inject_org_id],
    )
    return await client.get_tools()


async def load_all_tools(locale: str) -> list:
    if locale not in LANGUAGES:
        raise ValueError(f"Unsupported locale '{locale}'. Available: {', '.join(LANGUAGES)}")
    rag_tool = make_retrieve_context(locale)
    zoho_tools = await load_zoho_tools()
    return [rag_tool] + zoho_tools
