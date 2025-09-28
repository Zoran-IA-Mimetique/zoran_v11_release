from typing import Dict, Any, Literal, Optional, List
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class ProfileState(BaseModel):
    profiles: Dict[str, Dict[str, Any]] = {}

class ProfileManagerParams(BaseModel):
    action: Literal["add", "get", "list", "remove"]
    # État stateless
    current_profiles: ProfileState
    # Paramètres d'action
    profile_name: Optional[str] = None
    profile_config: Optional[Dict[str, Any]] = None

class ProfileManagerResult(BaseModel):
    action_performed: str
    updated_profiles: ProfileState
    result: Any

class ProfileManagerCapability(ExecutableCapability):
    """
    Gère une collection de profils de configuration nommés de manière stateless.
    L'état des profils est passé en paramètre à chaque appel.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.stateless_profile_manager",
            "name": "Stateless Profile Manager",
            "version": "2.0.0",
            "description": "Manages a collection of named configuration profiles statelessly.",
            "dependencies": ["pydantic"],
            "input_schema": ProfileManagerParams.model_json_schema(),
            "output_schema": ProfileManagerResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = ProfileManagerParams(**params)
        
        updated_profiles_state = p.current_profiles.copy(deep=True)
        action_result = None

        if p.action == "add":
            if p.profile_name is None or p.profile_config is None:
                raise ValueError("'profile_name' and 'profile_config' are required for 'add' action.")
            updated_profiles_state.profiles[p.profile_name] = p.profile_config
            action_result = {"status": "added", "profile_name": p.profile_name}

        elif p.action == "get":
            if p.profile_name is None:
                raise ValueError("'profile_name' is required for 'get' action.")
            action_result = {"profile_config": updated_profiles_state.profiles.get(p.profile_name)}

        elif p.action == "list":
            action_result = {"profile_names": list(updated_profiles_state.profiles.keys())}
            
        elif p.action == "remove":
            if p.profile_name is None:
                raise ValueError("'profile_name' is required for 'remove' action.")
            if p.profile_name in updated_profiles_state.profiles:
                del updated_profiles_state.profiles[p.profile_name]
                action_result = {"status": "removed", "profile_name": p.profile_name}
            else:
                action_result = {"status": "not_found", "profile_name": p.profile_name}

        else:
            raise ValueError(f"Unknown action: {p.action}")

        result = ProfileManagerResult(
            action_performed=p.action,
            updated_profiles=updated_profiles_state,
            result=action_result
        )
        return result.model_dump()
