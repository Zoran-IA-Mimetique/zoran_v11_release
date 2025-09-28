import numpy as np
from typing import Dict, Any, List
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class AttractorsParams(BaseModel):
    r: float = Field(3.7, ge=0, le=4.0, description="The 'r' parameter of the logistic map, controlling chaotic behavior.")
    initial_condition_x0: float = Field(0.5, ge=0, le=1.0)
    simulation_steps: int = Field(100, gt=0, le=10000)
    transient_steps: int = Field(100, ge=0, description="Number of initial steps to discard to focus on the attractor.")

class AttractorsResult(BaseModel):
    trajectory: List[float]
    final_state: float

class AttractorsCapability(ExecutableCapability):
    """
    Capacité de simulation de systèmes dynamiques simples, comme la carte logistique.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "math.dynamical_attractors",
            "name": "Dynamical System Attractors",
            "version": "2.0.0",
            "description": "Simulates the trajectory of the logistic map, a classic example of chaotic dynamics.",
            "dependencies": ["numpy", "pydantic"],
            "input_schema": AttractorsParams.model_json_schema(),
            "output_schema": AttractorsResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = AttractorsParams(**params)
        x = p.initial_condition_x0
        
        # Discard transient steps
        for _ in range(p.transient_steps):
            x = p.r * x * (1 - x)
            
        trajectory = []
        for _ in range(p.simulation_steps):
            x = p.r * x * (1 - x)
            trajectory.append(x)
        
        result = AttractorsResult(trajectory=trajectory, final_state=x)
        return result.model_dump()
