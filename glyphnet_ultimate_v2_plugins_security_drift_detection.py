from typing import Dict, Any, List
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

# Import optionnel, erreur levée uniquement à l'exécution si manquant
try:
    from scipy.stats import ks_2samp
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

class DriftDetectionParams(BaseModel):
    reference_distribution: conlist(float, min_length=2)
    new_data_distribution: conlist(float, min_length=2)
    significance_level: float = Field(0.05, gt=0, lt=1, alias="p_value_threshold")

class DriftDetectionResult(BaseModel):
    ks_statistic: float
    p_value: float
    is_drift_detected: bool
    interpretation: str

class DriftDetectionCapability(ExecutableCapability):
    """
    Détecte la dérive de distribution entre deux échantillons de données en utilisant
    le test de Kolmogorov-Smirnov à deux échantillons.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "security.data_drift_detection",
            "name": "Data Drift Detection (Kolmogorov-Smirnov)",
            "version": "2.0.0",
            "description": "Performs a two-sample Kolmogorov-Smirnov test to detect data distribution drift.",
            "dependencies": ["scipy", "pydantic"],
            "input_schema": DriftDetectionParams.model_json_schema(),
            "output_schema": DriftDetectionResult.model_json_schema()
        }
    
    def _check_scipy_installed(self):
        if not SCIPY_AVAILABLE:
            raise RuntimeError("The 'scipy' library is not installed. Please run 'pip install scipy'.")

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        self._check_scipy_installed()
        p = DriftDetectionParams(**params)
        
        statistic, p_value = ks_2samp(p.reference_distribution, p.new_data_distribution)
        drift_detected = p_value < p.significance_level

        interpretation = (
            f"The p-value ({p_value:.4f}) is {'less' if drift_detected else 'greater or equal'} "
            f"than the significance level ({p.significance_level}). "
            f"This suggests that the two distributions are statistically {'different (drift detected)' if drift_detected else 'similar (no drift detected)'}."
        )

        result = DriftDetectionResult(
            ks_statistic=float(statistic),
            p_value=float(p_value),
            is_drift_detected=drift_detected,
            interpretation=interpretation
        )
        return result.model_dump()
