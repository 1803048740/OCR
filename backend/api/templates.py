from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..services import template_service
from ..models.template import FieldMapping

router = APIRouter(prefix="/api/templates", tags=["templates"])


class CreateTemplateRequest(BaseModel):
    name: str
    description: str = ""
    reference_image_id: str = ""
    field_mappings: list[FieldMapping]
    excel_columns: list[str]


class UpdateTemplateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    field_mappings: Optional[list[FieldMapping]] = None
    excel_columns: Optional[list[str]] = None


@router.get("")
async def list_templates():
    return {"templates": [t.model_dump() for t in template_service.list_templates()]}


@router.get("/{template_id}")
async def get_template(template_id: str):
    t = template_service.get_template(template_id)
    if not t:
        raise HTTPException(404, "Template not found")
    return t.model_dump()


@router.post("")
async def create_template(req: CreateTemplateRequest):
    t = template_service.create_template(
        name=req.name,
        description=req.description,
        field_mappings=req.field_mappings,
        excel_columns=req.excel_columns,
        reference_image_id=req.reference_image_id,
    )
    return t.model_dump()


@router.put("/{template_id}")
async def update_template(template_id: str, req: UpdateTemplateRequest):
    updates = {k: v for k, v in req.model_dump().items() if v is not None}
    if req.field_mappings is not None:
        updates["field_mappings"] = [fm.model_dump() for fm in req.field_mappings]
    t = template_service.update_template(template_id, **updates)
    if not t:
        raise HTTPException(404, "Template not found")
    return t.model_dump()


@router.delete("/{template_id}")
async def delete_template(template_id: str):
    ok = template_service.delete_template(template_id)
    if not ok:
        raise HTTPException(404, "Template not found")
    return {"deleted": True}
