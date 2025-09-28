import random
from typing import Dict, Any, List, Tuple
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class ThompsonSamplingParams(BaseModel):
    # L'état est passé en paramètre, rendant la capacité stateless
    priors: List[Tuple[float, float]] = Field(description="List of (alpha, beta) priors for each arm's Beta distribution.")
    action: Literal["select_arm", "update"]
    # Paramètres pour l'action 'update'
    arm_to_update: Optional[int] = None
    reward_received: Optional[int] = Field(None, ge=0, le=1)

class ThompsonSamplingResult(BaseModel):
    action_performed: str
    result: Any

class ThompsonSamplingCapability(ExecutableCapability):
    """
    Capacité stateless pour le Thompson Sampling, une stratégie pour le
    problème du bandit manchot qui équilibre exploration et exploitation.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "decision.thompson_sampling",
            "name": "Thompson Sampling",
            "version": "2.0.0",
            "description": "Performs arm selection or updates priors for a multi-armed bandit problem using Thompson Sampling.",
            "dependencies": ["pydantic"],
            "input_schema": ThompsonSamplingParams.model_json_schema(),
            "output_schema": ThompsonSamplingResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = ThompsonSamplingParams(**params)

        if p.action == "select_arm":
            # Pour chaque bras, tirer un échantillon de sa distribution Beta(alpha, beta)
            samples = [random.betavariate(alpha, beta) for alpha, beta in p.priors]
            # Sélectionner le bras avec le plus haut échantillon
            selected_arm = max(range(len(samples)), key=lambda i: samples[i])
            action_result = {"selected_arm": selected_arm}
        
        elif p.action == "update":
            if p.arm_to_update is None or p.reward_received is None:
                raise ValueError("`arm_to_update` and `reward_received` are required for update action.")
            if p.arm_to_update >= len(p.priors):
                raise ValueError("`arm_to_update` index is out of bounds.")
            
            alpha, beta = p.priors[p.arm_to_update]
            
            # Mettre à jour les priors : alpha si récompense=1, beta si récompense=0
            new_priors = p.priors.copy()
            new_priors[p.arm_to_update] = (alpha + p.reward_received, beta + 1 - p.reward_received)
            action_result = {"updated_priors": new_priors}
            
        else:
            raise ValueError(f"Unknown action: {p.action}")

        result = ThompsonSamplingResult(action_performed=p.action, result=action_result)
        return result.model_dump()
