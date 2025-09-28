import statistics
from typing import Dict, Any, List, Literal
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class ConsensusManagerParams(BaseModel):
    values: conlist(float, min_length=1)
    method: Literal["mean", "median", "mode"] = "mean"

class ConsensusManagerResult(BaseModel):
    consensus_value: float

class ConsensusManagerCapability(ExecutableCapability):
    """
    Calcule une valeur de consensus à partir d'une liste de valeurs numériques.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.numerical_consensus",
            "name": "Numerical Consensus Manager",
            "version": "2.0.0",
            "description": "Calculates a consensus value from a list of numerical inputs.",
            "dependencies": ["pydantic"],
            "input_schema": ConsensusManagerParams.model_json_schema(),
            "output_schema": ConsensusManagerResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = ConsensusManagerParams(**params)

        if p.method == "mean":
            value = statistics.mean(p.values)
        elif p.method == "median":
            value = statistics.median(p.values)
        elif p.method == "mode":
            try:
                value = statistics.mode(p.values)
            except statistics.StatisticsError:
                # Si pas de mode unique, on retourne la moyenne
                value = statistics.mean(p.values)
        else:
            raise ValueError(f"Unknown consensus method: {p.method}")
            
        return ConsensusManagerResult(consensus_value=value).model_dump()
