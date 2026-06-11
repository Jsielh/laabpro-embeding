from pathlib import Path
from fastapi import APIRouter, HTTPException

from app.schemas.document import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
    DocumentListResponse,
    DocumentDeleteResponse,
    ReindexResponse,
)
from app.rag.document_service import (
    save_document,
    delete_document,
    list_documents,
    index_document,
    index_all_documents,
    AVAILABLE_LOCALES,
    DOCUMENTS_DIR,
)

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/locale/{locale}", response_model=DocumentListResponse)
def get_documents(locale: str):
    if locale not in AVAILABLE_LOCALES:
        raise HTTPException(status_code=400, detail=f"Invalid locale. Available: {AVAILABLE_LOCALES}")
    
    docs = list_documents(locale)
    return DocumentListResponse(
        documents=[DocumentResponse(**d) for d in docs],
        count=len(docs)
    )


@router.post("/", response_model=DocumentResponse)
def create_document(doc: DocumentCreate):
    filename = doc.filename if doc.filename else None
    try:
        saved_filename = save_document(doc.locale, doc.content, filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create document")
    
    doc_path = DOCUMENTS_DIR / doc.locale / saved_filename
    content = doc_path.read_text(encoding="utf-8")
    
    return DocumentResponse(
        filename=saved_filename,
        locale=doc.locale,
        content=content
    )


@router.put("/{locale}/{filename}", response_model=DocumentResponse)
def update_document(locale: str, filename: str, doc: DocumentUpdate):
    if locale not in AVAILABLE_LOCALES:
        raise HTTPException(status_code=400, detail=f"Invalid locale. Available: {AVAILABLE_LOCALES}")
    
    success = delete_document(locale, filename)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        save_document(locale, doc.content, filename)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update document")
    
    return DocumentResponse(
        filename=filename,
        locale=locale,
        content=doc.content
    )


@router.delete("/{locale}/{filename}", response_model=DocumentDeleteResponse)
def delete_doc(locale: str, filename: str):
    if locale not in AVAILABLE_LOCALES:
        raise HTTPException(status_code=400, detail=f"Invalid locale. Available: {AVAILABLE_LOCALES}")
    
    success = delete_document(locale, filename)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return DocumentDeleteResponse(
        deleted=True,
        filename=filename,
        message="Document deleted successfully"
    )


@router.post("/{locale}/{filename}/index", response_model=ReindexResponse)
def index_single_document(locale: str, filename: str):
    if locale not in AVAILABLE_LOCALES:
        raise HTTPException(status_code=400, detail=f"Invalid locale. Available: {AVAILABLE_LOCALES}")
    
    try:
        count = index_document(locale, filename)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to index document")
    
    return ReindexResponse(
        indexed=True,
        count=count,
        locale=locale,
        message=f"Indexed {count} chunks"
    )


@router.post("/reindex/{locale}", response_model=ReindexResponse)
def reindex_locale(locale: str):
    if locale not in AVAILABLE_LOCALES:
        raise HTTPException(status_code=400, detail=f"Invalid locale. Available: {AVAILABLE_LOCALES}")
    
    try:
        count = index_all_documents(locale)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to reindex documents")
    
    return ReindexResponse(
        indexed=True,
        count=count,
        locale=locale,
        message=f"Indexed {count} chunks from all documents"
    )