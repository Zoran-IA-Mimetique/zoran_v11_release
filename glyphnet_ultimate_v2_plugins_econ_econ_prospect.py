import numpy as np
from typing import Dict, Any
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class EconProspectParams(BaseModel):
    value: float = Field(..., description="The objective value of the outcome (positive for gain, negative for loss).")
    probability: float = Field(..., ge=0, le=1, description="The probability of the outcome occurring.")
    gain_sensitivity: float = Field(0.88, gt=0, alias="alpha")
    loss_sensitivity: float = Field(0.88, gt=0, alias="beta")
    loss_aversion: float = Field(2.25, gt=1, alias="lambda_")
    probability_weighting_param: float = Field(0.61, gt=0, alias="gamma")

class EconProspectResult(BaseModel):
    objective_value: float
    probability: float
    subjective_utility: float
    decision_weight: float
    final_prospect_value: float

class EconProspectCapability(ExecutableCapability):
    """
    Évalue un prospect unique (gain/perte) en utilisant les fonctions de la Théorie du Prospect.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "econ.prospect_theory_single",
            "name": "Single Prospect Evaluation",
            "version": "2.1.0",
            "description": "Evaluates a single prospect using Prospect Theory's value and probability weighting functions.",
            "dependencies": ["numpy", "pydantic"],
            "input_schema": EconProspectParams.model_json_schema(),
            "output_schema": EconProspectResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = EconProspectParams(**params)

        # 1. Calcul de l'utilité subjective (Value Function)
        if p.value >= 0:
            utility = p.value ** p.gain_sensitivity
        else:
            utility = -p.loss_aversion * ((-p.value) ** p.loss_sensitivity)

        # 2. Calcul du poids de décision (Probability Weighting Function - Prelec)
        # Note: ceci est une forme commune de la fonction de pondération.
        exp_term = (-np.log(p.probability)) ** p.probability_weighting_param
        weighting = np.exp(-exp_term)

        # 3. Calcul de la valeur finale du prospect
        final_value = utility * weighting

        result = EconProspectResult(
            objective_value=p.value,
            probability=p.probability,
            subjective_utility=utility,
            decision_weight=weighting,
            final_prospect_value=final_value
        )
        return result.model_dump()
