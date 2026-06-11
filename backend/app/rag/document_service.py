import re
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.utils.constants import CHUNK_SIZE, CHUNK_OVERLAP
from app.rag.vector_store import vector_stores

DOCUMENTS_DIR = Path(__file__).parent / "documents"

AVAILABLE_LOCALES = ["en", "es", "pt"]


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text


def get_documents_dir(locale: str) -> Path:
    locale_dir = DOCUMENTS_DIR / locale
    if not locale_dir.exists():
        locale_dir.mkdir(parents=True, exist_ok=True)
    return locale_dir


def save_document(locale: str, content: str, filename: str | None = None) -> str:
    if locale not in AVAILABLE_LOCALES:
        raise ValueError(f"Invalid locale: {locale}. Available: {AVAILABLE_LOCALES}")
    
    if filename:
        dangerous = ['..', '/', '\\', '\x00', '\n', '\r']
        if any(p in filename for p in dangerous):
            raise ValueError("Forbidden pattern in filename")
    
    doc_dir = get_documents_dir(locale)
    
    base_name = slugify(filename) if filename else "document"
    if not base_name.endswith(".txt"):
        base_name += ".txt"
    
    file_path = doc_dir / base_name
    
    counter = 1
    while file_path.exists():
        stem = file_path.stem
        file_path = doc_dir / f"{stem}_{counter}.txt"
        counter += 1
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return file_path.name


def delete_document(locale: str, filename: str) -> bool:
    if locale not in AVAILABLE_LOCALES:
        raise ValueError(f"Invalid locale: {locale}. Available: {AVAILABLE_LOCALES}")
    
    doc_dir = get_documents_dir(locale)
    file_path = doc_dir / filename
    
    if not file_path.exists():
        return False
    
    file_path.unlink()
    return True


def list_documents(locale: str) -> List[dict]:
    if locale not in AVAILABLE_LOCALES:
        raise ValueError(f"Invalid locale: {locale}. Available: {AVAILABLE_LOCALES}")
    
    doc_dir = get_documents_dir(locale)
    documents = []
    
    for doc_file in doc_dir.glob("*.txt"):
        try:
            with open(doc_file, "r", encoding="utf-8") as f:
                content = f.read()
            documents.append({
                "filename": doc_file.name,
                "locale": locale,
                "content": content
            })
        except (OSError, UnicodeDecodeError):
            pass
    
    return documents


def index_document(locale: str, filename: str) -> int:
    if locale not in AVAILABLE_LOCALES:
        raise ValueError(f"Invalid locale: {locale}. Available: {AVAILABLE_LOCALES}")
    
    doc_dir = get_documents_dir(locale)
    file_path = doc_dir / filename
    
    if not file_path.exists():
        raise FileNotFoundError(f"Document not found: {filename}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    doc = Document(
        page_content=content,
        metadata={"source": filename, "type": "txt"}
    )
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents([doc])
    
    vector_store = vector_stores.get(locale)
    if not vector_store:
        raise RuntimeError(f"Vector store not available for locale: {locale}")
    
    vector_store.add_documents(documents=chunks)
    
    return len(chunks)


def index_all_documents(locale: str) -> int:
    if locale not in AVAILABLE_LOCALES:
        raise ValueError(f"Invalid locale: {locale}. Available: {AVAILABLE_LOCALES}")
    
    docs = list_documents(locale)
    if not docs:
        return 0
    
    doc_objects = [
        Document(
            page_content=d["content"],
            metadata={"source": d["filename"], "type": "txt"}
        )
        for d in docs
    ]
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(doc_objects)
    
    vector_store = vector_stores.get(locale)
    if not vector_store:
        raise RuntimeError(f"Vector store not available for locale: {locale}")
    
    vector_store.add_documents(documents=chunks)
    
    return len(chunks)