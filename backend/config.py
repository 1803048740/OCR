from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
TEMPLATES_DIR = DATA_DIR / "templates"
EXPORTS_DIR = DATA_DIR / "exports"
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen3-vl:4b"
OLLAMA_TIMEOUT = 120.0

# Spatial matching threshold (normalized 0-1 coordinate space)
SPATIAL_MATCH_THRESHOLD = 0.15

for d in (UPLOADS_DIR, TEMPLATES_DIR, EXPORTS_DIR):
    d.mkdir(parents=True, exist_ok=True)
