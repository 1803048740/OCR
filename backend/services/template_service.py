import uuid
import math
from datetime import datetime
from ..models.template import Template, TemplateSummary, FieldMapping
from ..models.ocr_result import OCRResult, BoundingBox
from ..storage.file_store import FileStore
from ..config import TEMPLATES_DIR, SPATIAL_MATCH_THRESHOLD


_store = FileStore(TEMPLATES_DIR)


def _bbox_center(bbox: BoundingBox) -> tuple[float, float]:
    return bbox.center


def _distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def create_template(
    name: str,
    description: str,
    field_mappings: list[FieldMapping],
    excel_columns: list[str],
    reference_image_id: str = "",
) -> Template:
    now = datetime.now()
    template = Template(
        id=str(uuid.uuid4()),
        name=name,
        description=description,
        created_at=now,
        updated_at=now,
        reference_image_id=reference_image_id,
        field_mappings=field_mappings,
        excel_columns=excel_columns,
    )
    _store.save(template.id, template.model_dump(mode="json"))
    return template


def get_template(template_id: str) -> Template | None:
    data = _store.load(template_id)
    if data is None:
        return None
    return Template.model_validate(data)


def list_templates() -> list[TemplateSummary]:
    summaries = []
    for key in _store.list_keys():
        data = _store.load(key)
        if data:
            summaries.append(TemplateSummary(
                id=data["id"],
                name=data["name"],
                description=data.get("description", ""),
                created_at=data["created_at"],
                updated_at=data["updated_at"],
                field_count=len(data.get("field_mappings", [])),
            ))
    return summaries


def update_template(template_id: str, **kwargs) -> Template | None:
    template = get_template(template_id)
    if template is None:
        return None
    data = template.model_dump(mode="json")
    data.update(kwargs)
    data["updated_at"] = datetime.now().isoformat()
    _store.save(template_id, data)
    return Template.model_validate(data)


def delete_template(template_id: str) -> bool:
    return _store.delete(template_id)


def match_fields(template: Template, ocr_result: OCRResult) -> dict[str, dict]:
    """
    Spatial matching: for each FieldMapping anchor, find the nearest OCR field.
    Returns {excel_column: {text, confidence, field_id}}.
    """
    result: dict[str, dict] = {}
    used_ids: set[str] = set()

    for mapping in template.field_mappings:
        anchor_center = _bbox_center(mapping.bbox_anchor)
        best_field = None
        best_dist = float("inf")

        for field in ocr_result.fields:
            if field.id in used_ids:
                continue
            fc = _bbox_center(field.bbox)
            dist = _distance(anchor_center, fc)
            if dist < best_dist:
                best_dist = dist
                best_field = field

        if best_field and best_dist <= SPATIAL_MATCH_THRESHOLD:
            result[mapping.excel_column] = {
                "text": best_field.text,
                "confidence": best_field.confidence,
                "field_id": best_field.id,
            }
            used_ids.add(best_field.id)

    return result
