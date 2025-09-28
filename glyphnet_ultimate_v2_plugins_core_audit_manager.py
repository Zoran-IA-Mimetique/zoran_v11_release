import time
import hashlib
import json
from typing import Dict, Any, List, Literal, Optional
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class AuditEntry(BaseModel):
    actor: str
    action: str
    target: str
    timestamp: float
    entry_hash: str

class AuditState(BaseModel):
    audit_trail: List[AuditEntry] = []

class AuditManagerParams(BaseModel):
    action: Literal["record", "verify_trail"]
    current_state: AuditState
    actor: Optional[str] = None
    action_name: Optional[str] = Field(None, alias="action_to_record")
    target: Optional[str] = None

class AuditManagerResult(BaseModel):
    action_performed: str
    updated_state: AuditState
    result: Any

class AuditManagerCapability(ExecutableCapability):
    """
    Gère un journal d'audit simple et haché de manière stateless.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.stateless_audit_manager",
            "name": "Stateless Audit Manager",
            "version": "2.0.0",
            "description": "Manages a simple, hashed audit trail statelessly.",
            "dependencies": ["pydantic"],
            "input_schema": AuditManagerParams.model_json_schema(),
            "output_schema": AuditManagerResult.model_json_schema()
        }

    def _hash_entry(self, entry_data: Dict[str, Any]) -> str:
        entry_string = json.dumps(entry_data, sort_keys=True).encode("utf-8")
        return hashlib.sha256(entry_string).hexdigest()

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = AuditManagerParams(**params)
        updated_state = p.current_state.copy(deep=True)
        action_result = None

        if p.action == "record":
            if not all([p.actor, p.action_name, p.target]):
                raise ValueError("'actor', 'action_name', and 'target' are required for 'record' action.")
            
            entry_data = {
                "actor": p.actor,
                "action": p.action_name,
                "target": p.target,
                "timestamp": time.time()
            }
            entry = AuditEntry(**entry_data, entry_hash=self._hash_entry(entry_data))
            updated_state.audit_trail.append(entry)
            action_result = entry

        elif p.action == "verify_trail":
            is_valid = True
            for entry in updated_state.audit_trail:
                entry_data = entry.model_dump(exclude={"entry_hash"})
                if self._hash_entry(entry_data) != entry.entry_hash:
                    is_valid = False
                    break
            action_result = {"is_trail_valid": is_valid}

        result = AuditManagerResult(
            action_performed=p.action,
            updated_state=updated_state,
            result=action_result
        )
        return result.model_dump()
