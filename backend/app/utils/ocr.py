import base64
import io

from PIL import Image
from openai import OpenAI

from app.core.settings import settings


_client = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


def _image_to_base64(content: bytes) -> str:
    image = Image.open(io.BytesIO(content))
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def extract_text_from_image(content: bytes) -> str:
    if not settings.OCR_ENABLED:
        return ""

    try:
        b64 = _image_to_base64(content)
    except Exception:
        return ""

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract all text from this image. Return only the extracted text, nothing else."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
                    ]
                }
            ],
            max_tokens=4096
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return ""


def extract_text_from_pdf_pages(pdf_path: str) -> str:
    if not settings.OCR_ENABLED:
        return ""

    import fitz

    doc = fitz.open(pdf_path)
    images = []

    try:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=300)
            img_bytes = pix.tobytes("png")
            b64 = base64.b64encode(img_bytes).decode("utf-8")
            images.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{b64}"}
            })
    except Exception:
        return ""
    finally:
        doc.close()

    if not images:
        return ""

    PAGE_BATCH_SIZE = 3
    fragments = []
    client = _get_client()

    for start in range(0, len(images), PAGE_BATCH_SIZE):
        batch = images[start:start + PAGE_BATCH_SIZE]
        page_nums = ", ".join(
            str(i + 1) for i in range(start, min(start + PAGE_BATCH_SIZE, len(images)))
        )
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"Extract all text from PDF page(s) {page_nums}. Return only the extracted text, nothing else."},
                            *batch
                        ]
                    }
                ],
                max_tokens=4096
            )
            fragments.append(response.choices[0].message.content.strip())
        except Exception:
            fragments.append("")

    return "\n\n".join(f for f in fragments if f)
