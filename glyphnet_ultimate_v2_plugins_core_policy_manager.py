from typing import Dict, Any, Literal, Optional
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class PolicyState(BaseModel):
    policies: Dict[str, Dict[str, Any]] = {}

class PolicyManagerParams(BaseModel):
    action: Literal["add", "evaluate", "remove"]
    current_state: PolicyState
    policy_name: str
    rules: Optional[Dict[str, Any]] = None # For 'add'
    context: Optional[Dict[str, Any]] = None # For 'evaluate'

class PolicyEvaluationResult(BaseModel):
    policy_name: str
    is_valid: bool
    violation_reason: Optional[str] = None

class PolicyManagerResult(BaseModel):
    action_performed: str
    updated_state: PolicyState
    result: Any

class PolicyManagerCapability(ExecutableCapability):
    """
    Gère et évalue des politiques simples (ensembles de règles clé-valeur) de manière stateless.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.stateless_policy_manager",
            "name": "Stateless Policy Manager",
            "version": "2.0.0",
            "description": "Manages and evaluates simple key-value policies statelessly.",
            "dependencies": ["pydantic"],
            "input_schema": PolicyManagerParams.model_json_schema(),
            "output_schema": PolicyManagerResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = PolicyManagerParams(**params)
        updated_state = p.current_state.copy(deep=True)
        action_result = None

        if p.action == "add":
            if p.rules is None:
                raise ValueError("'rules' are required for 'add' action.")
            updated_state.policies[p.policy_name] = p.rules
            action_result = {"status": "added", "policy_name": p.policy_name}

        elif p.action == "evaluate":
            if p.context is None:
                raise ValueError("'context' is required for 'evaluate' action.")
            rules = updated_state.policies.get(p.policy_name, {})
            if not rules:
                 action_result = PolicyEvaluationResult(policy_name=p.policy_name, is_valid=False, violation_reason="Policy not found.")
            else:
                for key, expected_value in rules.items():
                    if p.context.get(key) != expected_value:
                        action_result = PolicyEvaluationResult(
                            policy_name=p.policy_name,
                            is_valid=False,
                            violation_reason=f"Failed rule for key '{key}'. Expected '{expected_value}', got '{p.context.get(key)}'."
                        )
                        break
                else: # Si la boucle se termine sans break
                    action_result = PolicyEvaluationResult(policy_name=p.policy_name, is_valid=True)
        
        elif p.action == "remove":
            if p.policy_name in updated_state.policies:
                del updated_state.policies[p.policy_name]
                action_result = {"status": "removed"}
            else:
                action_result = {"status": "not_found"}

        result = PolicyManagerResult(
            action_performed=p.action,
            updated_state=updated_state,
            result=action_result
        )
        return result.model_dump()
