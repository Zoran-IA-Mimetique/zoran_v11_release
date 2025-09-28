import numpy as np
from typing import Dict, Any, List
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class GroupPolarizationParams(BaseModel):
    initial_opinions: conlist(float, min_length=2) = Field(description="List of opinions, typically in range [-1, 1].")
    amplification_factor: float = Field(0.1, ge=0, description="How much opinions are pushed towards extremes at each step.")
    simulation_steps: int = Field(5, gt=0)

class GroupPolarizationResult(BaseModel):
    opinion_history: List[List[float]]
    initial_mean_opinion: float
    final_mean_opinion: float
    initial_std_dev: float
    final_std_dev: float

class GroupPolarizationCapability(ExecutableCapability):
    """
    Simule la polarisation de groupe, où les opinions des membres deviennent plus extrêmes.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "social.group_polarization",
            "name": "Group Polarization Simulation",
            "version": "2.0.0",
            "description": "Simulates how group discussion can lead to more extreme opinions.",
            "dependencies": ["numpy", "pydantic"],
            "input_schema": GroupPolarizationParams.model_json_schema(),
            "output_schema": GroupPolarizationResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = GroupPolarizationParams(**params)
        
        opinions = np.array(p.initial_opinions)
        history = [opinions.tolist()]
        initial_stats = {"mean": np.mean(opinions), "std": np.std(opinions)}

        for _ in range(p.simulation_steps):
            group_mean = np.mean(opinions)
            # Les opinions supérieures à la moyenne deviennent plus positives, les autres plus négatives.
            opinions = np.where(
                opinions >= group_mean,
                opinions + p.amplification_factor,
                opinions - p.amplification_factor
            )
            # Borner les opinions à [-1, 1]
            opinions = np.clip(opinions, -1.0, 1.0)
            history.append(opinions.tolist())

        final_stats = {"mean": np.mean(opinions), "std": np.std(opinions)}
        
        result = GroupPolarizationResult(
            opinion_history=history,
            initial_mean_opinion=initial_stats["mean"],
            final_mean_opinion=final_stats["mean"],
            initial_std_dev=initial_stats["std"],
            final_std_dev=final_stats["std"]
        )
        return result.model_dump()
