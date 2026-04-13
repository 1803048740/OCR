from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services import ocr_service
from ..api.images import _find_image

router = APIRouter(prefix="/api/ocr", tags=["ocr"])


class RecognizeRequest(BaseModel):
    image_id: str
    engine: str = "paddleocr"


@router.get("/engines")
async def list_engines():
    return {"engines": ocr_service.list_engines()}


@router.post("/recognize")
async def recognize(req: RecognizeRequest):
    image_path = _find_image(req.image_id)
    if not image_path:
        raise HTTPException(404, f"Image not found: {req.image_id}")
    try:
        result = await ocr_service.recognize(str(image_path), req.engine)
        return result.model_dump()
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"OCR failed: {e}")
