from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .ocr_result import BoundingBox


class FieldMapping(BaseModel):
    field_label: str
    excel_column: str
    bbox_anchor: BoundingBox  # normalized position on reference image
    regex_pattern: Optional[str] = None


class Template(BaseModel):
    id: str
    name: str
    description: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    reference_image_id: str = ""
    field_mappings: list[FieldMapping] = []
    excel_columns: list[str] = []


class TemplateSummary(BaseModel):
    id: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    field_count: int
