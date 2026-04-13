from abc import ABC, abstractmethod
from ..models.ocr_result import OCRResult


class OCREngine(ABC):
    @abstractmethod
    async def recognize(self, image_path: str) -> OCRResult:
        """Run OCR, return normalized result (coords 0.0-1.0)."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Check if engine is ready."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...
