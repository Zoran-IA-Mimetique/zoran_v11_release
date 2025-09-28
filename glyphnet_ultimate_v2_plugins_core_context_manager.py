from typing import Dict, Any, Literal
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class ContextState(BaseModel):
    context_data: Dict[str, Any] = {}

class ContextManagerParams(BaseModel):
    action: Literal["set", "get", "update", "dump"]
    current_state: ContextState
    key: Optional[str] = None
    value: Optional[Any] = None
    update_data: Optional[Dict[str, Any]] = None

class ContextManagerResult(BaseModel):
    action_performed: str
    updated_state: ContextState
    result: Any

class ContextManagerCapability(ExecutableCapability):
    """
    Gère un contexte (dictionnaire clé-valeur) de manière stateless.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.stateless_context_manager",
            "name": "Stateless Context Manager",
            "version": "2.0.0",
            "description": "Manages a key-value context object statelessly.",
            "dependencies": ["pydantic"],
            "input_schema": ContextManagerParams.model_json_schema(),
            "output_schema": ContextManagerResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = ContextManagerParams(**params)
        updated_state = p.current_state.copy(deep=True)
        action_result = None

        if p.action == "set":
            if p.key is None:
                raise ValueError("'key' is required for 'set' action.")
            updated_state.context_data[p.key] = p.value
            action_result = {"status": "set", "key": p.key}
        
        elif p.action == "get":
            if p.key is None:
                raise ValueError("'key' is required for 'get' action.")
            action_result = {"value": updated_state.context_data.get(p.key)}
            
        elif p.action == "update":
            if p.update_data is None:
                raise ValueError("'update_data' is required for 'update' action.")
            updated_state.context_data.update(p.update_data)
            action_result = {"status": "updated"}
        
        elif p.action == "dump":
            action_result = updated_state.context_data
            
        result = ContextManagerResult(
            action_performed=p.action,
            updated_state=updated_state,
            result=action_result
        )
        return result.model_dump()
