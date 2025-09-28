import random
from typing import Dict, Any, List
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class OpinionDynamicsParams(BaseModel):
    num_agents: int = Field(10, gt=1)
    simulation_steps: int = Field(5, gt=0)
    influence_probability: float = Field(0.3, ge=0, le=1, description="Probability of an agent being influenced by another.")

class OpinionDynamicsResult(BaseModel):
    opinion_history: List[List[int]]
    final_opinion_distribution: Dict[str, int]

class OpinionDynamicsCapability(ExecutableCapability):
    """
    Capacité simulant la dynamique d'opinion simple (modèle de Deffuant).
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "social.opinion_dynamics",
            "name": "Opinion Dynamics Simulation",
            "version": "2.0.0",
            "description": "Simulates a simple opinion spreading model (Deffuant-like).",
            "dependencies": ["pydantic"],
            "input_schema": OpinionDynamicsParams.model_json_schema(),
            "output_schema": OpinionDynamicsResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = OpinionDynamicsParams(**params)
        
        opinions = [random.choice([-1, 1]) for _ in range(p.num_agents)]
        history = [opinions.copy()]

        for _ in range(p.simulation_steps):
            new_opinions = opinions.copy()
            # Sélectionner un agent à mettre à jour
            agent_to_update_idx = random.randrange(p.num_agents)
            
            if random.random() < p.influence_probability:
                # Choisir un influenceur au hasard
                influencer_idx = random.randrange(p.num_agents)
                # L'agent adopte l'opinion de l'influenceur
                new_opinions[agent_to_update_idx] = opinions[influencer_idx]
            
            opinions = new_opinions
            history.append(opinions.copy())

        result = OpinionDynamicsResult(
            opinion_history=history,
            final_opinion_distribution={"-1": opinions.count(-1), "1": opinions.count(1)}
        )
        return result.model_dump()
