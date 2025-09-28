import numpy as np
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class PredictiveCodingParams(BaseModel):
    time_series: conlist(float, min_length=2)
    window_size: int = Field(3, gt=0)

class PredictiveCodingResult(BaseModel):
    prediction: Optional[float]
    model_coefficients: Optional[List[float]]
    model_error: Optional[float]

class PredictiveCodingCapability(ExecutableCapability):
    """
    Capacité de prédiction simple basée sur un modèle autorégressif.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "math.predictive_coding",
            "name": "Simple Predictive Coding",
            "version": "2.0.0",
            "description": "Predicts the next value in a series using a simple autoregressive model.",
            "dependencies": ["numpy", "pydantic"],
            "input_schema": PredictiveCodingParams.model_json_schema(),
            "output_schema": PredictiveCodingResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = PredictiveCodingParams(**params)
        
        if len(p.time_series) <= p.window_size:
            return PredictiveCodingResult(prediction=None, model_coefficients=None, model_error=None).model_dump()

        # Préparer les données pour la régression
        X = np.array([p.time_series[i : i + p.window_size] for i in range(len(p.time_series) - p.window_size)])
        y = np.array(p.time_series[p.window_size:])

        # Résoudre par moindres carrés
        coeffs, residuals, _, _ = np.linalg.lstsq(X, y, rcond=None)
        
        # Faire une prédiction
        last_window = np.array(p.time_series[-p.window_size:])
        prediction = float(np.dot(last_window, coeffs))
        
        error = float(residuals[0]) if residuals.size > 0 else 0.0

        result = PredictiveCodingResult(
            prediction=prediction,
            model_coefficients=coeffs.tolist(),
            model_error=error
        )
        return result.model_dump()
