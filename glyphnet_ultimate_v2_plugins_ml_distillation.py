import numpy as np
from typing import Dict, Any, List
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class DistillationParams(BaseModel):
    logits_from_teachers: conlist(List[float], min_length=1)

class DistillationResult(BaseModel):
    ensembled_logits: List[float]
    student_probabilities: List[float]

class DistillationCapability(ExecutableCapability):
    """
    Réalise une distillation de connaissances simple en moyennant les logits de
    plusieurs modèles "professeurs" pour créer une cible pour un modèle "étudiant".
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "ml.knowledge_distillation_logits",
            "name": "Knowledge Distillation (Logits Averaging)",
            "version": "2.0.0",
            "description": "Performs simple knowledge distillation by averaging teacher model logits.",
            "dependencies": ["numpy", "pydantic"],
            "input_schema": DistillationParams.model_json_schema(),
            "output_schema": DistillationResult.model_json_schema()
        }
        
    def _softmax(self, x: np.ndarray) -> np.ndarray:
        """Helper to compute softmax."""
        e_x = np.exp(x - np.max(x)) # Soustraire max pour la stabilité numérique
        return e_x / e_x.sum(axis=0)

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = DistillationParams(**params)
        
        logits_array = np.array(p.logits_from_teachers)
        
        # Vérifier que tous les vecteurs de logits ont la même longueur
        if len(set(len(row) for row in logits_array)) > 1:
            raise ValueError("All logits vectors must have the same length.")

        # Moyenne des logits sur l'axe des professeurs
        mean_logits = logits_array.mean(axis=0)
        
        # Calculer les probabilités de l'étudiant à partir des logits moyennés
        student_probs = self._softmax(mean_logits)

        result = DistillationResult(
            ensembled_logits=mean_logits.tolist(),
            student_probabilities=student_probs.tolist()
        )
        return result.model_dump()
