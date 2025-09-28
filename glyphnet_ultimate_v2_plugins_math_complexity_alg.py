import zlib
from typing import Dict, Any
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class ComplexityAlgParams(BaseModel):
    data: str

class ComplexityAlgResult(BaseModel):
    original_size_bytes: int
    compressed_size_bytes: int
    compression_ratio: float

class ComplexityAlgCapability(ExecutableCapability):
    """
    Capacité approximant la complexité de Kolmogorov d'une chaîne de caractères
    via la taille de sa version compressée.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "math.kolmogorov_complexity_approx",
            "name": "Kolmogorov Complexity Approximation",
            "version": "2.0.0",
            "description": "Approximates Kolmogorov complexity via zlib compression.",
            "dependencies": ["pydantic"],
            "input_schema": ComplexityAlgParams.model_json_schema(),
            "output_schema": ComplexityAlgResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = ComplexityAlgParams(**params)
        
        if not p.data:
            return ComplexityAlgResult(
                original_size_bytes=0,
                compressed_size_bytes=len(zlib.compress(b'')),
                compression_ratio=0
            ).model_dump()
            
        encoded_data = p.data.encode("utf-8")
        original_size = len(encoded_data)
        compressed_data = zlib.compress(encoded_data)
        compressed_size = len(compressed_data)

        result = ComplexityAlgResult(
            original_size_bytes=original_size,
            compressed_size_bytes=compressed_size,
            compression_ratio=original_size / compressed_size if compressed_size > 0 else 0
        )
        return result.model_dump()
