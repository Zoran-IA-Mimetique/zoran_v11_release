import numpy as np
from typing import Dict, Any, List
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

# Import optionnel
try:
    from sklearn.isotonic import IsotonicRegression
    from sklearn.calibration import calibration_curve
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

class CalibrationCheckParams(BaseModel):
    true_labels: conlist(int, min_length=10)
    predicted_probabilities: conlist(float, min_length=10)
    n_bins: int = Field(10, gt=1)

class CalibrationCheckResult(BaseModel):
    calibrated_probabilities: List[float]
    calibration_curve_true_prob: List[float]
    calibration_curve_pred_prob: List[float]

class CalibrationCheckCapability(ExecutableCapability):
    """
    Évalue et corrige la calibration des probabilités d'un classifieur
    en utilisant la régression isotonique.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "security.classifier_calibration",
            "name": "Classifier Calibration Check (Isotonic)",
            "version": "2.0.0",
            "description": "Checks and recalibrates classifier probabilities using Isotonic Regression.",
            "dependencies": ["scikit-learn", "numpy", "pydantic"],
            "input_schema": CalibrationCheckParams.model_json_schema(),
            "output_schema": CalibrationCheckResult.model_json_schema()
        }

    def _check_sklearn_installed(self):
        if not SKLEARN_AVAILABLE:
            raise RuntimeError("The 'scikit-learn' library is not installed. Please run 'pip install scikit-learn'.")

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        self._check_sklearn_installed()
        p = CalibrationCheckParams(**params)
        
        if len(p.true_labels) != len(p.predicted_probabilities):
            raise ValueError("Label and probability lists must have the same length.")

        y_true = np.array(p.true_labels)
        y_prob = np.array(p.predicted_probabilities)

        # Calibrer les probabilités
        ir = IsotonicRegression(out_of_bounds="clip")
        calibrated_probs = ir.fit_transform(y_prob, y_true)
        
        # Générer la courbe de calibration pour l'analyse
        prob_true, prob_pred = calibration_curve(y_true, calibrated_probs, n_bins=p.n_bins)

        result = CalibrationCheckResult(
            calibrated_probabilities=calibrated_probs.tolist(),
            calibration_curve_true_prob=prob_true.tolist(),
            calibration_curve_pred_prob=prob_pred.tolist()
        )
        return result.model_dump()
