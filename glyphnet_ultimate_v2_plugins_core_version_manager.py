import hashlib
import json
from typing import Dict, Any, Literal, Optional
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class VersionedData(BaseModel):
    data: Dict[str, Any]
    sha256_hash: str

class VersionState(BaseModel):
    versions: Dict[str, VersionedData] = {}

class VersionManagerParams(BaseModel):
    action: Literal["add", "get"]
    current_state: VersionState
    version_name: str
    data_to_version: Optional[Dict[str, Any]] = None

class VersionManagerResult(BaseModel):
    action_performed: str
    updated_state: VersionState
    result: Any

class VersionManagerCapability(ExecutableCapability):
    """
    Gère des versions nommées et hachées de documents JSON de manière stateless.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.stateless_version_manager",
            "name": "Stateless Version Manager",
            "version": "2.0.0",
            "description": "Manages named and hashed versions of JSON documents statelessly.",
            "dependencies": ["pydantic"],
            "input_schema": VersionManagerParams.model_json_schema(),
            "output_schema": VersionManagerResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = VersionManagerParams(**params)
        updated_state = p.current_state.copy(deep=True)
        action_result = None

        if p.action == "add":
            if p.data_to_version is None:
                raise ValueError("'data_to_version' is required for 'add' action.")
            
            data_string = json.dumps(p.data_to_version, sort_keys=True).encode("utf-8")
            data_hash = hashlib.sha256(data_string).hexdigest()
            
            version_entry = VersionedData(data=p.data_to_version, sha256_hash=data_hash)
            updated_state.versions[p.version_name] = version_entry
            action_result = {"version_name": p.version_name, "hash": data_hash}
            
        elif p.action == "get":
            action_result = updated_state.versions.get(p.version_name)

        result = VersionManagerResult(action_performed=p.action, updated_state=updated_state, result=action_result)
        return result.model_dump()
