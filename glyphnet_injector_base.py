"""GlyphNet core - injector base class"""
from typing import Any, Dict
import time, json

class GlyphInjectorBase:
    """Base class for GlyphNet-augmented injectors."""
    def __init__(self, name: str):
        self.name = name

    def audit(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    def emit_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        event.setdefault("injector", self.name)
        event.setdefault("ts", time.time())
        return event
