import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from ..config import UPLOADS_DIR

router = APIRouter(prefix="/api/images", tags=["images"])

ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff", ".tif"}


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    suffix = Path(file.filename or "img.jpg").suffix.lower()
    if suffix not in ALLOWED_EXTS:
        raise HTTPException(400, f"Unsupported file type: {suffix}")
    image_id = uuid.uuid4().hex
    dest = UPLOADS_DIR / f"{image_id}{suffix}"
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"image_id": image_id, "filename": file.filename}


@router.get("/{image_id}")
async def get_image(image_id: str):
    for ext in ALLOWED_EXTS:
        path = UPLOADS_DIR / f"{image_id}{ext}"
        if path.exists():
            return FileResponse(str(path))
    raise HTTPException(404, "Image not found")


def _find_image(image_id: str) -> Path | None:
    for ext in ALLOWED_EXTS:
        path = UPLOADS_DIR / f"{image_id}{ext}"
        if path.exists():
            return path
    return None
