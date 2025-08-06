import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

QDRANT_URL = os.getenv("QDRANT_URL")
VECTOR_COLLECTION_NAME = "pdf_chunks"
