import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.exceptions import NotFittedError
from typing import Dict, Any, List
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class CausalDiscoveryParams(BaseModel):
    potential_cause_series: conlist(float, min_length=2, alias="x")
    potential_effect_series: conlist(float, min_length=2, alias="y")
    lag: int = Field(1, gt=0)

class CausalDiscoveryResult(BaseModel):
    granger_r2_score: float
    model_coefficients: List[float]
    interpretation: str

class CausalDiscoveryCapability(ExecutableCapability):
    """
    Teste une causalité de Granger simple (si le passé de X aide à prédire Y).
    NOTE: La causalité de Granger n'est pas une vraie causalité, mais une prédictibilité.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "math.causal_discovery_granger",
            "name": "Granger Causality Test",
            "version": "1.0.0-alpha",
            "description": "Performs a simple Granger causality test to check if one time series predicts another. (Proof of Concept)",
            "dependencies": ["scikit-learn", "numpy", "pydantic"],
            "input_schema": CausalDiscoveryParams.model_json_schema(),
            "output_schema": CausalDiscoveryResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = CausalDiscoveryParams(**params)
        
        if len(p.potential_cause_series) != len(p.potential_effect_series):
            raise ValueError("Time series must have the same length.")
        
        if len(p.potential_cause_series) <= p.lag:
            raise ValueError("Time series length must be greater than the lag.")

        # Préparer les données : prédire Y(t) à partir de X(t-1)...X(t-lag)
        X_data = np.array([p.potential_cause_series[i-p.lag : i] for i in range(p.lag, len(p.potential_cause_series))])
        y_data = np.array(p.potential_effect_series[p.lag:])
        
        try:
            model = LinearRegression().fit(X_data, y_data)
            score = model.score(X_data, y_data)
        except NotFittedError as e:
            raise RuntimeError(f"Model fitting failed: {e}")
            
        interpretation = (
            f"The past {p.lag} value(s) of the cause series can explain "
            f"{score:.2%} of the variance in the effect series. "
            "A higher score suggests stronger predictive power."
        )

        result = CausalDiscoveryResult(
            granger_r2_score=float(score),
            model_coefficients=model.coef_.tolist(),
            interpretation=interpretation
        )
        return result.model_dump()
