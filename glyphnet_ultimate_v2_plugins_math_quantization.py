import numpy as np
from typing import Dict, Any, List, Literal
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class QuantizationParams(BaseModel):
    tensor: conlist(float, min_length=1)
    mode: Literal["int8", "fp8"] = "int8"

class QuantizationResult(BaseModel):
    mode: str
    quantized_tensor: List[Any] # Peut être int ou float
    scale_factor: Optional[float] = None
    zero_point: Optional[int] = None

class QuantizationCapability(ExecutableCapability):
    """
    Quantifie un tenseur de nombres flottants vers des types de données
    de plus faible précision comme int8 ou fp8 (simulé).
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "math.tensor_quantization",
            "name": "Tensor Quantization",
            "version": "2.0.0",
            "description": "Quantizes a float tensor to lower precision formats like int8.",
            "dependencies": ["numpy", "pydantic"],
            "input_schema": QuantizationParams.model_json_schema(),
            "output_schema": QuantizationResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = QuantizationParams(**params)
        arr = np.array(p.tensor, dtype=np.float32)

        if p.mode == "int8":
            # Quantization affinée simple (min/max scaling)
            min_val, max_val = arr.min(), arr.max()
            scale = (max_val - min_val) / 255 if (max_val - min_val) > 1e-9 else 1.0
            zero_point = -128 - (min_val / scale)
            
            quantized = np.clip(np.round(arr / scale + zero_point), -128, 127).astype(np.int8)
            
            result = QuantizationResult(
                mode=p.mode,
                quantized_tensor=quantized.tolist(),
                scale_factor=scale,
                zero_point=int(zero_point)
            )

        elif p.mode == "fp8":
            # La simulation la plus proche avec numpy est float16
            quantized = arr.astype(np.float16)
            result = QuantizationResult(
                mode=p.mode,
                quantized_tensor=quantized.tolist()
            )
            
        else:
            raise ValueError(f"Unsupported quantization mode: {p.mode}")

        return result.model_dump()
