from typing import Dict, Any, List, Set
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class FrameNetParams(BaseModel):
    text: str

class FrameNetResult(BaseModel):
    detected_frames: List[str]

class FrameNetCapability(ExecutableCapability):
    """
    Capacité de détection de cadres sémantiques (frames) simple via mots-clés.
    NOTE: Ceci est une simulation. Une vraie implémentation utiliserait une base de données
    lexicale comme FrameNet de Berkeley.
    """
    # Les cadres et mots-clés devraient être chargés depuis une configuration externe.
    FRAMES_KB: Dict[str, Set[str]] = {
        "commerce_transaction": {"buy", "sell", "trade", "market", "purchase", "pay"},
        "motion": {"run", "walk", "fly", "move", "go", "travel"},
        "communication": {"say", "tell", "ask", "explain", "speak", "inform"},
        "judgment": {"blame", "praise", "judge", "accuse", "forgive"}
    }

    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "nlp.frame_detection",
            "name": "Semantic Frame Detection (Keyword-based)",
            "version": "1.0.0-alpha",
            "description": "Detects semantic frames in text using a simple keyword knowledge base. (Proof of Concept)",
            "dependencies": ["pydantic"],
            "input_schema": FrameNetParams.model_json_schema(),
            "output_schema": FrameNetResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = FrameNetParams(**params)
        
        detected_frames = set()
        # Tokenisation simple et passage en minuscules pour la correspondance
        words = set(p.text.lower().split())

        for frame, keywords in self.FRAMES_KB.items():
            if not keywords.isdisjoint(words):
                detected_frames.add(frame)
        
        result = FrameNetResult(detected_frames=sorted(list(detected_frames)))
        return result.model_dump()
