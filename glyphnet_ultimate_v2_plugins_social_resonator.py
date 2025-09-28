import statistics
from typing import Dict, Any, List, Literal
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class ResonatorParams(BaseModel):
    votes: conlist(int, min_length=1) = Field(description="List of binary votes (0 for No, 1 for Yes).")
    method: Literal["majority", "mean", "unanimity"] = Field("majority")

class ResonatorResult(BaseModel):
    method_used: str
    consensus_result: int
    details: Dict[str, Any]

class ResonatorCapability(ExecutableCapability):
    """
    Capacité pour des algorithmes de consensus simples sur des votes binaires.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "social.simple_consensus",
            "name": "Simple Consensus Algorithms",
            "version": "2.0.0",
            "description": "Calculates consensus on binary votes using majority, mean, or unanimity rules.",
            "dependencies": ["pydantic"],
            "input_schema": ResonatorParams.model_json_schema(),
            "output_schema": ResonatorResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = ResonatorParams(**params)
        
        result = 0
        details = {
            "total_votes": len(p.votes),
            "yes_votes": p.votes.count(1),
            "no_votes": p.votes.count(0)
        }

        if p.method == "majority":
            result = 1 if details["yes_votes"] >= details["no_votes"] else 0
        elif p.method == "mean":
            # Le seuil de 0.5 est standard pour la moyenne
            result = 1 if statistics.mean(p.votes) >= 0.5 else 0
        elif p.method == "unanimity":
            result = 1 if all(v == 1 for v in p.votes) else 0

        final_result = ResonatorResult(
            method_used=p.method,
            consensus_result=result,
            details=details
        )
        return final_result.model_dump()
