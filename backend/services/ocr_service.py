from ..engines.paddle_engine import PaddleOCREngine
from ..engines.qwen_engine import QwenEngine
from ..engines.base import OCREngine
from ..models.ocr_result import OCRResult


_engines: dict[str, OCREngine] = {
    "paddleocr": PaddleOCREngine(),
    "qwen3vl": QwenEngine(),
}


def get_engine(name: str) -> OCREngine:
    engine = _engines.get(name)
    if not engine:
        raise ValueError(f"Unknown engine: {name}")
    return engine


def list_engines() -> list[dict]:
    result = []
    for name, engine in _engines.items():
        result.append({
            "name": name,
            "available": engine.is_available(),
        })
    return result


async def recognize(image_path: str, engine_name: str) -> OCRResult:
    engine = get_engine(engine_name)
    return await engine.recognize(image_path)
