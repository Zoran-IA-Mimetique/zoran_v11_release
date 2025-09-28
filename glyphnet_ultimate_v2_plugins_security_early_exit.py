import numpy as np
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class EarlyExitParams(BaseModel):
    confidence_scores: conlist(float, min_length=1) = Field(description="A sequence of confidence scores from a cascading pipeline.")
    confidence_threshold: float = Field(0.9, ge=0, le=1)

class EarlyExitResult(BaseModel):
    can_exit_early: bool
    first_exit_point_index: Optional[int]
    exit_confidence_score: Optional[float]

class EarlyExitCapability(ExecutableCapability):
    """
    Détermine si un pipeline en cascade peut s'arrêter prématurément si
    la confiance d'une étape intermédiaire dépasse un seuil.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "security.pipeline_early_exit",
            "name": "Pipeline Early Exit Check",
            "version": "2.0.0",
            "description": "Checks if a pipeline can exit early based on intermediate confidence scores.",
            "dependencies": ["numpy", "pydantic"],
            "input_schema": EarlyExitParams.model_json_schema(),
            "output_schema": EarlyExitResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = EarlyExitParams(**params)

        confidences = np.array(p.confidence_scores)
        # Trouver le premier index où la confiance dépasse le seuil
        exit_indices = np.where(confidences >= p.confidence_threshold)[0]

        if exit_indices.size > 0:
            first_exit_index = int(exit_indices[0])
            result = EarlyExitResult(
                can_exit_early=True,
                first_exit_point_index=first_exit_index,
                exit_confidence_score=p.confidence_scores[first_exit_index]
            )
        else:
            result = EarlyExitResult(
                can_exit_early=False,
                first_exit_point_index=None,
                exit_confidence_score=None
            )

        return result.model_dump()
