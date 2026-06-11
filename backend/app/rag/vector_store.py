import chromadb
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from app.core.settings import settings
embeddings = OpenAIEmbeddings()

client = chromadb.CloudClient(
  api_key=settings.CHROMA_API_KEY,
  tenant=settings.CHROMA_TENANT,
  database=settings.CHROMA_DATABASE
)

LANGUAGES = ["en", "es", "pt"]

vector_stores = {
    lang: Chroma(
        client=client,
        collection_name=f"laabpro-{lang}",
        embedding_function=embeddings
    )
    for lang in LANGUAGES
}
