import numpy as np
from typing import Dict, Any, List
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class EntropyMaximizationParams(BaseModel):
    values: conlist(float, min_length=1)

class EntropyMaximizationResult(BaseModel):
    max_entropy_distribution: List[float]
    shannon_entropy: float

class EntropyMaximizationCapability(ExecutableCapability):
    """
    Capacité qui transforme un vecteur de poids non négatifs en une
    distribution de probabilité qui maximise l'entropie (distribution uniforme).
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "math.entropy_maximization",
            "name": "Entropy Maximization",
            "version": "2.0.0",
            "description": "Normalizes a vector into a probability distribution (uniform-like).",
            "dependencies": ["numpy", "pydantic"],
            "input_schema": EntropyMaximizationParams.model_json_schema(),
            "output_schema": EntropyMaximizationResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = EntropyMaximizationParams(**params)
        
        arr = np.array(p.values, dtype=float)
        if np.any(arr < 0):
            raise ValueError("Input values cannot be negative for this normalization method.")

        # Ajoute un epsilon pour la stabilité si tous les poids sont nuls
        arr += 1e-9
        
        distribution = arr / np.sum(arr)
        
        # Calculer l'entropie de la distribution résultante
        entropy = -np.sum(distribution * np.log2(distribution))
        
        result = EntropyMaximizationResult(
            max_entropy_distribution=distribution.tolist(),
            shannon_entropy=float(entropy)
        )
        return result.model_dump()
