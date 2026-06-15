from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    FRONTEND_URL: str = "http://localhost:5173"
    OPENAI_API_KEY: str
    CHROMA_HOST: str = "api.trychroma.com"
    CHROMA_API_KEY: str
    CHROMA_TENANT: str
    CHROMA_DATABASE: str
    ZOHO_MCP_SERVER_URL: str
    ZOHO_DESK_ORG_ID: int
    ZOHO_DESK_DEPARTMENT_ID: int
    OCR_ENABLED: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
