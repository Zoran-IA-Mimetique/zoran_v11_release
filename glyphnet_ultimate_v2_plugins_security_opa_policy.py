import json
from typing import Dict, Any
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class OPAPolicyParams(BaseModel):
    policy: Dict[str, Any] = Field(description="A simplified OPA-like policy, represented as a dictionary of required key-value pairs.")
    input_data: Dict[str, Any] = Field(description="The input data to be evaluated against the policy.")

class OPAPolicyResult(BaseModel):
    is_allowed: bool
    violation_reason: Optional[str] = None

class OPAPolicyCapability(ExecutableCapability):
    """
    Évalue un ensemble de données d'entrée par rapport à une politique de sécurité
    simplifiée, inspirée par Open Policy Agent (OPA).
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "security.simple_opa_policy_evaluation",
            "name": "Simple OPA-like Policy Evaluation",
            "version": "2.0.0",
            "description": "Evaluates input data against a simple key-value policy.",
            "dependencies": ["pydantic"],
            "input_schema": OPAPolicyParams.model_json_schema(),
            "output_schema": OPAPolicyResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = OPAPolicyParams(**params)
        
        for required_key, required_value in p.policy.items():
            if required_key not in p.input_data:
                return OPAPolicyResult(
                    is_allowed=False,
                    violation_reason=f"Required key '{required_key}' is missing from input data."
                ).model_dump()
            
            if p.input_data[required_key] != required_value:
                return OPAPolicyResult(
                    is_allowed=False,
                    violation_reason=f"For key '{required_key}', expected value '{required_value}', but got '{p.input_data[required_key]}'."
                ).model_dump()

        return OPAPolicyResult(is_allowed=True).model_dump()
