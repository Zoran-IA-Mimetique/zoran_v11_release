import numpy as np
from typing import Dict, Any, List
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class InformationFlowParams(BaseModel):
    source_series: conlist(int, min_length=2)
    target_series: conlist(int, min_length=2)
    history_length: int = Field(1, gt=0, alias="k")

class InformationFlowResult(BaseModel):
    transfer_entropy: float

class InformationFlowCapability(ExecutableCapability):
    """
    Calcule une approximation simple de l'entropie de transfert, une mesure
    du flux d'information dirigé entre deux séries temporelles.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "math.information_flow",
            "name": "Transfer Entropy Approximation",
            "version": "1.0.0-alpha",
            "description": "Calculates a simple approximation of transfer entropy between two discrete time series. (Proof of Concept)",
            "dependencies": ["numpy", "pydantic"],
            "input_schema": InformationFlowParams.model_json_schema(),
            "output_schema": InformationFlowResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = InformationFlowParams(**params)
        
        if len(p.source_series) != len(p.target_series):
            raise ValueError("Source and target series must have the same length.")

        # Implémentation simplifiée de l'entropie de transfert pour des séries discrètes
        # H(Y_t+1 | Y_t) - H(Y_t+1 | Y_t, X_t)
        # Ceci est une version très basique qui ne calcule qu'une partie de la formule.
        # Une implémentation réelle utiliserait des bibliothèques spécialisées (JIDT, etc.)
        
        # Calcul de H(Y_t+1 | Y_t, X_t)
        joint_counts = {}
        total_transitions = len(p.source_series) - p.history_length
        if total_transitions <= 0:
            return InformationFlowResult(transfer_entropy=0.0).model_dump()

        for i in range(total_transitions):
            source_context = tuple(p.source_series[i : i + p.history_length])
            target_context = tuple(p.target_series[i : i + p.history_length])
            outcome = p.target_series[i + p.history_length]
            
            key = (source_context, target_context, outcome)
            joint_counts[key] = joint_counts.get(key, 0) + 1

        probs = np.array(list(joint_counts.values())) / total_transitions
        entropy = -np.sum(probs * np.log2(probs))

        return InformationFlowResult(transfer_entropy=float(entropy)).model_dump()
