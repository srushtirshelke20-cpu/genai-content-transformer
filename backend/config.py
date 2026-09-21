import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "exports"

# Auto-create the exports folder if it doesn't exist
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

# Ollama local configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_TAGS_URL = os.getenv("OLLAMA_TAGS_URL", "http://localhost:11434/api/tags")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama3.1")

# CORS Allowed Origins (Allow Vite React on 5173, Next.js on 3000, etc.)
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]
