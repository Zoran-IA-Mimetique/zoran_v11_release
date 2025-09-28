import random
from typing import Dict, Any, List
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class AnthroMimeticParams(BaseModel):
    num_agents: int = Field(10, gt=1)
    simulation_steps: int = Field(5, gt=0)
    num_traits: int = Field(6, gt=1, description="Number of distinct cultural traits (e.g., from 0 to 5).")
    imitation_probability: float = Field(0.5, ge=0, le=1, description="Probability for an agent to imitate another.")

class AnthroMimeticResult(BaseModel):
    simulation_history: List[List[int]]
    final_traits_distribution: Dict[int, int]

class AnthroMimeticCapability(ExecutableCapability):
    """
    Capacité simulant un processus d'imitation culturelle simple (anthropologie mimétique).
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "social.anthro_mimetic",
            "name": "Anthropological Mimetic Simulation",
            "version": "2.0.0",
            "description": "Simulates a simple process of cultural trait imitation within a population.",
            "dependencies": ["pydantic"],
            "input_schema": AnthroMimeticParams.model_json_schema(),
            "output_schema": AnthroMimeticResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = AnthroMimeticParams(**params)

        traits = [random.randint(0, p.num_traits - 1) for _ in range(p.num_agents)]
        history = [traits.copy()]

        for _ in range(p.simulation_steps):
            new_traits = []
            for current_trait in traits:
                if random.random() < p.imitation_probability:
                    # Agent imite un autre agent choisi au hasard
                    new_traits.append(random.choice(traits))
                else:
                    # Agent conserve son trait actuel
                    new_traits.append(current_trait)
            traits = new_traits
            history.append(traits.copy())

        final_distribution = {i: traits.count(i) for i in range(p.num_traits)}
        result = AnthroMimeticResult(
            simulation_history=history,
            final_traits_distribution=final_distribution
        )
        return result.model_dump()
