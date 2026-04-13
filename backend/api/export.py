from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from ..models.export import ExportRequest, ExportRow
from ..services import template_service, ocr_service, export_service
from ..api.images import _find_image

router = APIRouter(prefix="/api/export", tags=["export"])


async def _process_batch(image_ids: list[str], template_id: str, engine: str = "paddleocr"):
    template = template_service.get_template(template_id)
    if not template:
        raise HTTPException(404, "Template not found")

    rows: list[ExportRow] = []
    for image_id in image_ids:
        path = _find_image(image_id)
        if not path:
            rows.append(ExportRow(image_id=image_id, columns={}, confidence_scores={}))
            continue
        try:
            ocr_result = await ocr_service.recognize(str(path), engine)
            matched = template_service.match_fields(template, ocr_result)
            columns = {col: info["text"] for col, info in matched.items()}
            scores = {col: info["confidence"] for col, info in matched.items()}
            rows.append(ExportRow(image_id=image_id, columns=columns, confidence_scores=scores))
        except Exception:
            rows.append(ExportRow(image_id=image_id, columns={}, confidence_scores={}))

    return template, rows


@router.post("/excel")
async def export_excel(req: ExportRequest):
    template, rows = await _process_batch(req.image_ids, req.template_id)
    path = export_service.generate_excel(template.excel_columns, rows)
    return FileResponse(
        str(path),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=req.output_filename or path.name,
    )


@router.post("/batch")
async def batch_export(req: ExportRequest):
    template, rows = await _process_batch(req.image_ids, req.template_id)
    path = export_service.generate_excel(template.excel_columns, rows)
    return FileResponse(
        str(path),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=req.output_filename or path.name,
    )


@router.post("/preview")
async def preview_export(req: ExportRequest):
    """Return matched fields as JSON without generating Excel."""
    template, rows = await _process_batch(req.image_ids, req.template_id)
    return {
        "columns": template.excel_columns,
        "rows": [r.model_dump() for r in rows],
    }
