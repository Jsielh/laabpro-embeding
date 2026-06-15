from pathlib import Path
import logging

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.rag.rag_system import create_agent_locale
from app.constants import CORS_CONFIG, INFO_MESSAGES
from app.api import chat, documents

logger = logging.getLogger(__name__)

app = FastAPI(title="LaabPro Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_CONFIG["ALLOW_ORIGINS"],
    allow_credentials=CORS_CONFIG["ALLOW_CREDENTIALS"],
    allow_methods=CORS_CONFIG["ALLOW_METHODS"],
    allow_headers=CORS_CONFIG["ALLOW_HEADERS"],
)

app.include_router(chat.router)
app.include_router(documents.router)


widget_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
logger.info("Widget dist path: %s | exists: %s", widget_dist, widget_dist.exists())

if widget_dist.exists():
    app.mount("/widget", StaticFiles(directory=str(widget_dist)), name="widget")
    logger.info("Static files mounted at /widget")
else:
    logger.warning("Widget dist NOT FOUND at %s", widget_dist)


@app.get("/widget/laabpro-widget.js")
async def serve_widget_js():
    widget_path = widget_dist / "laabpro-widget.js"
    if not widget_path.exists():
        raise HTTPException(status_code=404, detail="Widget JS not found")
    return FileResponse(widget_path, media_type="application/javascript")

class QueryRequest(BaseModel):
    query: str
    locale: str
    session_id: str

class QueryResponse(BaseModel):
    answer: str


@app.get("/")
def read_root():
    return {"message": "LaabPro Agent API", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "ok", "message": INFO_MESSAGES["HEALTH"]}


@app.post("/ask", response_model=QueryResponse)
async def ask(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        agent = await create_agent_locale(request.locale)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Internal configuration error")
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Failed to initialize agent")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        final_message = None
        thread_id = f"{request.locale}:{request.session_id}"
        async for event in agent.astream(
            {"messages": [{"role": "user", "content": request.query}]},
            config={"configurable": {"thread_id": thread_id}},
            stream_mode="values",
        ):
            final_message = event["messages"][-1]

        if final_message is None:
            raise HTTPException(status_code=500, detail="Agent returned no response")

        return QueryResponse(answer=final_message.content)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error processing query: {e}")
