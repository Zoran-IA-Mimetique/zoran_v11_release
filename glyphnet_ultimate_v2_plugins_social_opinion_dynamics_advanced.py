import random
from typing import Dict, Any, List
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class BoundedConfidenceParams(BaseModel):
    initial_opinions: conlist(float, min_length=2) = Field(
        description="List of initial opinions, typically in the range [0, 1]."
    )
    confidence_threshold: float = Field(0.2, gt=0, alias="epsilon", description="The maximum distance between opinions for interaction to occur.")
    simulation_steps: int = Field(10, gt=0)

class BoundedConfidenceResult(BaseModel):
    opinion_history: List[List[float]]
    final_opinions: List[float]
    number_of_clusters: int

class OpinionDynamicsAdvancedCapability(ExecutableCapability):
    """
    Capacité simulant la dynamique d'opinion avec un modèle de confiance bornée (Deffuant-Weisbuch).
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "social.opinion_dynamics_bounded_confidence",
            "name": "Bounded Confidence Opinion Dynamics",
            "version": "2.0.0",
            "description": "Simulates the Deffuant-Weisbuch model of bounded confidence.",
            "dependencies": ["pydantic"],
            "input_schema": BoundedConfidenceParams.model_json_schema(),
            "output_schema": BoundedConfidenceResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute la simulation de confiance bornée."""
        p = BoundedConfidenceParams(**params)
        
        opinions = p.initial_opinions.copy()
        num_agents = len(opinions)
        history = [opinions.copy()]

        for _ in range(p.simulation_steps * num_agents): # Assurer que chaque agent a une chance d'interagir en moyenne par étape
            # Choisir deux agents au hasard pour une interaction potentielle
            i, j = random.sample(range(num_agents), 2)
            
            # Si leurs opinions sont suffisamment proches, ils convergent
            if abs(opinions[i] - opinions[j]) < p.confidence_threshold:
                # La formule de convergence standard (mu=0.5)
                avg = (opinions[i] + opinions[j]) / 2
                opinions[i] = avg
                opinions[j] = avg
            
            # Enregistrer l'état après chaque interaction
            history.append(opinions.copy())
        
        # Calculer le nombre de clusters d'opinion à la fin
        rounded_opinions = [round(op, 3) for op in opinions] # Arrondir pour grouper les opinions très proches
        num_clusters = len(set(rounded_opinions))

        result = BoundedConfidenceResult(
            opinion_history=history,
            final_opinions=opinions,
            number_of_clusters=num_clusters
        )
        return result.model_dump()
