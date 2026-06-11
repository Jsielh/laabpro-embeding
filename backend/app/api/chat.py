import logging
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

logger = logging.getLogger(__name__)

from app.rag.rag_system import create_agent_locale
from app.utils.constants import (
    IMAGE_EXTENSIONS,
    PDF_SCANNED_THRESHOLD,
    SUPPORTED_EXTENSIONS,
)

router = APIRouter(prefix="/chat", tags=["chat"])


def _extract_text(content: bytes, filename: str) -> str:
    ext = Path(filename).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Supported: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

    if ext == ".txt":
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail=f"File '{filename}' contains invalid UTF-8 encoding"
            )

    if ext == ".pdf":
        import pymupdf4llm
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        try:
            try:
                pages = pymupdf4llm.to_markdown(tmp_path, page_chunks=True)
                text = "\n\n".join(
                    p.get("text", "") for p in pages if p.get("text", "").strip()
                )
            except Exception:
                logger.warning("pymupdf4llm failed for '%s', falling back to OCR", filename)
                text = ""
            if len(text.strip()) >= PDF_SCANNED_THRESHOLD:
                return text
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        from app.utils.ocr import extract_text_from_pdf_pages
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        try:
            return extract_text_from_pdf_pages(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    if ext in IMAGE_EXTENSIONS:
        from app.utils.ocr import extract_text_from_image
        return extract_text_from_image(content)

    if ext == ".docx":
        import docx
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        try:
            document = docx.Document(tmp_path)
            return "\n".join(p.text for p in document.paragraphs)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    return ""


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    query: str = Form(""),
    session_id: str = Form(...),
    locale: str = Form(...),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    content = await file.read()
    extracted_text = _extract_text(content, file.filename)

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="No extractable text found in the file")

    try:
        agent = await create_agent_locale(locale)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Internal configuration error")
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Failed to initialize agent")
    except ValueError as e:
        logger.warning("ValueError initializing agent for locale '%s': %s", locale, e)
        raise HTTPException(status_code=400, detail="Invalid configuration for the requested locale")

    combined = f"[FILE NAME: {file.filename}]\n[FILE CONTENT]:\n{extracted_text}\n\n"
    if query.strip():
        combined += f"User question: {query}"

    try:
        final_message = None
        thread_id = f"{locale}:{session_id}"
        async for event in agent.astream(
            {"messages": [{"role": "user", "content": combined}]},
            config={"configurable": {"thread_id": thread_id}},
            stream_mode="values",
        ):
            final_message = event["messages"][-1]

        if final_message is None:
            raise HTTPException(status_code=500, detail="Agent returned no response")

        return {
            "answer": final_message.content,
            "filename": file.filename,
            "extracted_text": extracted_text,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error processing file '%s' for locale '%s'", file.filename, locale)
        raise HTTPException(status_code=500, detail="Internal error processing file")
