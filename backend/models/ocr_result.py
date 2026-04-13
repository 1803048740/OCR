from pydantic import BaseModel, Field
from typing import Optional


class BoundingBox(BaseModel):
    """Four corner points normalized to [0.0, 1.0] relative to image dimensions."""
    points: list[list[float]]  # [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]

    @property
    def center(self) -> tuple[float, float]:
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        return (sum(xs) / len(xs), sum(ys) / len(ys))

    @property
    def x_min(self) -> float:
        return min(p[0] for p in self.points)

    @property
    def y_min(self) -> float:
        return min(p[1] for p in self.points)

    @property
    def x_max(self) -> float:
        return max(p[0] for p in self.points)

    @property
    def y_max(self) -> float:
        return max(p[1] for p in self.points)


class TextField(BaseModel):
    id: str
    text: str
    confidence: float = Field(ge=0.0, le=1.0)
    bbox: BoundingBox
    label: Optional[str] = None  # user-assigned semantic label


class OCRResult(BaseModel):
    image_id: str
    engine: str  # "paddleocr" | "qwen3vl"
    image_width: int
    image_height: int
    fields: list[TextField]
