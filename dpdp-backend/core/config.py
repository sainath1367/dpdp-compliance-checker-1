import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MODEL_NAME = os.getenv("MODEL_NAME", "all-MiniLM-L6-v2")
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 35))
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dpdp_compliance.db")
    USE_EXTERNAL_API = os.getenv("USE_EXTERNAL_API", "false").lower() == "true"
    EXTERNAL_API_KEY = os.getenv("EXTERNAL_API_KEY", "")

settings = Settings()

USE_EXTERNAL_API = settings.USE_EXTERNAL_API
EXTERNAL_API_KEY = settings.EXTERNAL_API_KEY