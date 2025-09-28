import spacy
from typing import Dict, Any, List
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

_NLP_MODELS_LP = {} # Cache séparé pour ce plugin

class LangPerformParams(BaseModel):
    text: str = Field(..., min_length=1)
    model: str = Field("en_core_web_sm")

class LangPerformResult(BaseModel):
    token_count: int
    parts_of_speech: List[str]
    dependencies: List[str]
    average_token_length: float

class LangPerformCapability(ExecutableCapability):
    """
    Capacité analysant les aspects performatifs d'un texte (POS, dépendances).
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "nlp.language_performance",
            "name": "Language Performance Analysis",
            "version": "2.0.0",
            "description": "Analyzes performative aspects of language like POS and dependency parsing.",
            "dependencies": ["spacy", "pydantic"],
            "input_schema": LangPerformParams.model_json_schema(),
            "output_schema": LangPerformResult.model_json_schema()
        }

    def _load_model(self, model_name: str):
        if model_name not in _NLP_MODELS_LP:
            try:
                _NLP_MODELS_LP[model_name] = spacy.load(model_name)
            except OSError:
                raise ImportError(f"SpaCy model '{model_name}' not found. Please run 'python -m spacy download {model_name}'")
        return _NLP_MODELS_LP[model_name]

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = LangPerformParams(**params)
        nlp = self._load_model(p.model)
        doc = nlp(p.text)

        tokens = [token.text for token in doc]
        if not tokens:
            return LangPerformResult(token_count=0, parts_of_speech=[], dependencies=[], average_token_length=0.0).model_dump()

        avg_len = sum(len(t) for t in tokens) / len(tokens)

        result = LangPerformResult(
            token_count=len(tokens),
            parts_of_speech=[token.pos_ for token in doc],
            dependencies=[token.dep_ for token in doc],
            average_token_length=avg_len
        )
        return result.model_dump()
