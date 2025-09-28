import numpy as np
from scipy.integrate import odeint
from typing import Dict, Any, List, Tuple
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class DynamicalSystemsParams(BaseModel):
    system: str = Field("lorenz", description="The dynamical system to simulate.")
    initial_state: Tuple[float, float, float] = Field((1.0, 1.0, 1.0))
    duration: float = Field(10.0, gt=0)
    time_steps: int = Field(1000, gt=10)
    # Paramètres spécifiques au système de Lorenz
    sigma: float = Field(10.0)
    beta: float = Field(8/3)
    rho: float = Field(28.0)

class DynamicalSystemsResult(BaseModel):
    time_vector: List[float]
    trajectory: List[List[float]]

class DynamicalSystemsCapability(ExecutableCapability):
    """
    Capacité de simulation de systèmes dynamiques continus comme l'attracteur de Lorenz.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "math.dynamical_systems",
            "name": "Dynamical Systems Simulator",
            "version": "2.0.0",
            "description": "Simulates continuous dynamical systems like the Lorenz attractor.",
            "dependencies": ["numpy", "scipy", "pydantic"],
            "input_schema": DynamicalSystemsParams.model_json_schema(),
            "output_schema": DynamicalSystemsResult.model_json_schema()
        }

    def _lorenz_equations(self, state, t, sigma, beta, rho):
        x, y, z = state
        dxdt = sigma * (y - x)
        dydt = x * (rho - z) - y
        dzdt = x * y - beta * z
        return [dxdt, dydt, dzdt]

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = DynamicalSystemsParams(**params)

        if p.system == "lorenz":
            time_vector = np.linspace(0, p.duration, p.time_steps)
            solution = odeint(
                self._lorenz_equations,
                p.initial_state,
                time_vector,
                args=(p.sigma, p.beta, p.rho)
            )
        else:
            raise ValueError(f"Dynamical system '{p.system}' is not supported.")

        result = DynamicalSystemsResult(
            time_vector=time_vector.tolist(),
            trajectory=solution.tolist()
        )
        return result.model_dump()
