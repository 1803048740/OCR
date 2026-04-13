import uuid
import base64
import json
import re
from pathlib import Path
from PIL import Image
import httpx
from ..models.ocr_result import OCRResult, TextField, BoundingBox
from .base import OCREngine
from ..config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT


SYSTEM_PROMPT = (
    "You are an OCR assistant. Analyze the receipt/invoice image and extract ALL text fields. "
    "Return a JSON array ONLY, with no markdown or explanation. "
    "Each element must have: {\"text\": \"...\", \"bbox\": [x_min, y_min, x_max, y_max]} "
    "where coordinates are integers in the 0-1000 normalized space "
    "(0,0 = top-left, 1000,1000 = bottom-right)."
)


class QwenEngine(OCREngine):
    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_MODEL):
        self.base_url = base_url.rstrip("/")
        self.model = model

    @property
    def name(self) -> str:
        return "qwen3vl"

    def is_available(self) -> bool:
        try:
            r = httpx.get(f"{self.base_url}/api/tags", timeout=3.0)
            if r.status_code == 200:
                models = [m.get("name", "") for m in r.json().get("models", [])]
                return any(self.model in m for m in models)
            return False
        except Exception:
            return False

    async def recognize(self, image_path: str) -> OCRResult:
        img = Image.open(image_path)
        w, h = img.size
        image_id = Path(image_path).stem

        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()

        payload = {
            "model": self.model,
            "messages": [{
                "role": "user",
                "content": SYSTEM_PROMPT,
                "images": [b64],
            }],
            "stream": False,
        }

        async with httpx.AsyncClient(timeout=OLLAMA_TIMEOUT) as client:
            resp = await client.post(f"{self.base_url}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()

        content = data.get("message", {}).get("content", "")
        fields = self._parse_response(content)

        # Normalize 0-1000 → 0-1
        result_fields: list[TextField] = []
        for item in fields:
            bbox = item.get("bbox", [])
            if len(bbox) == 4:
                x1, y1, x2, y2 = [c / 1000.0 for c in bbox]
                points = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
            else:
                points = [[0, 0], [1, 0], [1, 1], [0, 1]]
            result_fields.append(TextField(
                id=str(uuid.uuid4()),
                text=item.get("text", ""),
                confidence=item.get("confidence", 0.9),
                bbox=BoundingBox(points=points),
            ))

        return OCRResult(
            image_id=image_id,
            engine=self.name,
            image_width=w,
            image_height=h,
            fields=result_fields,
        )

    def _parse_response(self, content: str) -> list[dict]:
        # Strip <think>...</think> blocks (Qwen3 chain-of-thought)
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
        # Try direct JSON parse
        try:
            data = json.loads(content)
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass
        # Extract first JSON array from text
        m = re.search(r"\[.*\]", content, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                pass
        return []
