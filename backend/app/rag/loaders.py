from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pymupdf4llm

from app.utils.constants import CHUNK_SIZE, CHUNK_OVERLAP, DOCUMENTS_DIR, IMAGE_EXTENSIONS, PDF_SCANNED_THRESHOLD
from app.utils.ocr import extract_text_from_image, extract_text_from_pdf_pages


def process_documents(locale: str) -> List[Document]:
    all_docs: List[Document] = []
    path = Path(f"{DOCUMENTS_DIR}/{locale}")

    if not path.exists():
        return []

    for doc_txt in path.glob("*.txt"):
        try:
            with open(doc_txt, "r", encoding="utf-8") as f:
                content = f.read()
            all_docs.append(Document(
                page_content=content,
                metadata={"source": doc_txt.name, "type": "txt"}
            ))
        except (OSError, UnicodeDecodeError):
            pass

    for doc_pdf in path.glob("*.pdf"):
        try:
            pages = pymupdf4llm.to_markdown(str(doc_pdf), page_chunks=True)
            pdf_text = "\n".join(
                p.get("text", "") for p in (pages or []) if p.get("text", "").strip()
            )
            if len(pdf_text.strip()) >= PDF_SCANNED_THRESHOLD:
                for page in pages:
                    text = page.get("text", "").strip()
                    if text:
                        all_docs.append(Document(
                            page_content=text,
                            metadata={
                                "source": doc_pdf.name,
                                "page": page.get("metadata", {}).get("page", 0),
                                "type": "pdf"
                            }
                        ))
            else:
                scanned_text = extract_text_from_pdf_pages(str(doc_pdf))
                if scanned_text.strip():
                    all_docs = [d for d in all_docs if d.metadata.get("source") != doc_pdf.name]
                    all_docs.append(Document(
                        page_content=scanned_text,
                        metadata={"source": doc_pdf.name, "type": "pdf_ocr"}
                    ))
        except Exception:
            try:
                scanned_text = extract_text_from_pdf_pages(str(doc_pdf))
                if scanned_text.strip():
                    all_docs = [d for d in all_docs if d.metadata.get("source") != doc_pdf.name]
                    all_docs.append(Document(
                        page_content=scanned_text,
                        metadata={"source": doc_pdf.name, "type": "pdf_ocr"}
                    ))
            except Exception:
                pass

    for ext in (f"*{e}" for e in IMAGE_EXTENSIONS):
        for doc_img in path.glob(ext):
            try:
                content = extract_text_from_image(doc_img.read_bytes())
                if content.strip():
                    all_docs.append(Document(
                        page_content=content,
                        metadata={"source": doc_img.name, "type": "image"}
                    ))
            except Exception:
                pass

    if not all_docs:
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(all_docs)

    return chunks
