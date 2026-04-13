from pydantic import BaseModel
from typing import Optional


class ExportRequest(BaseModel):
    image_ids: list[str]
    template_id: str
    output_filename: Optional[str] = "export.xlsx"


class ExportRow(BaseModel):
    image_id: str
    columns: dict[str, str]
    confidence_scores: dict[str, float] = {}
