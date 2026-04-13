from fastapi import APIRouter
from .ocr import router as ocr_router
from .images import router as images_router
from .templates import router as templates_router
from .export import router as export_router

api_router = APIRouter()
api_router.include_router(ocr_router)
api_router.include_router(images_router)
api_router.include_router(templates_router)
api_router.include_router(export_router)
