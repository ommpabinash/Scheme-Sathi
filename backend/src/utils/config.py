import os
from dotenv import load_dotenv

# Load .env file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=env_path)

class Settings:
    # Server Configurations
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")

    # Storage Directories
    BASE_DIR: str = BASE_DIR
    RAW_PDFS_DIR: str = os.path.join(BASE_DIR, os.getenv("RAW_PDFS_DIR", "data/raw_pdfs"))
    PROCESSED_DATA_DIR: str = os.path.join(BASE_DIR, os.getenv("PROCESSED_DATA_DIR", "data/processed"))
    CHROMA_PERSIST_DIR: str = os.path.join(BASE_DIR, os.getenv("CHROMA_PERSIST_DIR", "vectorstore"))

    # RAG & Routing Configurations
    COSINE_SIMILARITY_THRESHOLD: float = float(os.getenv("COSINE_SIMILARITY_THRESHOLD", 0.70))
    TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", 4))

settings = Settings()

# Ensure directories exist
os.makedirs(settings.RAW_PDFS_DIR, exist_ok=True)
os.makedirs(settings.PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
