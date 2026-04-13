import json
from pathlib import Path
from typing import Any


class FileStore:
    def __init__(self, directory: Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def save(self, key: str, data: dict) -> None:
        path = self.directory / f"{key}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def load(self, key: str) -> dict | None:
        path = self.directory / f"{key}.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def list_keys(self) -> list[str]:
        return [p.stem for p in sorted(self.directory.glob("*.json"))]

    def delete(self, key: str) -> bool:
        path = self.directory / f"{key}.json"
        if path.exists():
            path.unlink()
            return True
        return False

    def exists(self, key: str) -> bool:
        return (self.directory / f"{key}.json").exists()
