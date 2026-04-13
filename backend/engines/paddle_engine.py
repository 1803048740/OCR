import asyncio
import uuid
from pathlib import Path
from PIL import Image
from ..models.ocr_result import OCRResult, TextField, BoundingBox
from .base import OCREngine


class PaddleOCREngine(OCREngine):
    def __init__(self):
        self._ocr = None

    def _get_ocr(self):
        if self._ocr is None:
            from paddleocr import PaddleOCR
            self._ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)
        return self._ocr

    @property
    def name(self) -> str:
        return "paddleocr"

    def is_available(self) -> bool:
        try:
            from paddleocr import PaddleOCR  # noqa
            return True
        except ImportError:
            return False

    def _run_ocr(self, image_path: str):
        return self._get_ocr().ocr(image_path, cls=True)

    async def recognize(self, image_path: str) -> OCRResult:
        img = Image.open(image_path)
        w, h = img.size
        image_id = Path(image_path).stem

        raw = await asyncio.to_thread(self._run_ocr, image_path)

        fields: list[TextField] = []
        if raw and raw[0]:
            for line in raw[0]:
                if not line:
                    continue
                bbox_points, text_info = line[0], line[1]
                text = text_info[0]
                conf = float(text_info[1])
                # Normalize pixel coords → 0-1
                norm_points = [[pt[0] / w, pt[1] / h] for pt in bbox_points]
                fields.append(TextField(
                    id=str(uuid.uuid4()),
                    text=text,
                    confidence=conf,
                    bbox=BoundingBox(points=norm_points),
                ))

        return OCRResult(
            image_id=image_id,
            engine=self.name,
            image_width=w,
            image_height=h,
            fields=fields,
        )
