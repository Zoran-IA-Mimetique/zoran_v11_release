"""Simple audit logger writing newline-delimited JSON events."""
import json, os
from typing import Dict

class AuditLogger:
    def __init__(self, path: str):
        self.path = path
        # ensure directory
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    def log_event(self, event: Dict):
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, ensure_ascii=False) + "\n")
