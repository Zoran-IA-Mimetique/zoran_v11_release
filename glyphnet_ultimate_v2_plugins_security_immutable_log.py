import hashlib
import time
import json
from typing import Dict, Any, List, Literal, Optional
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class ImmutableLogParams(BaseModel):
    action: Literal["append", "verify"]
    # État actuel de la chaîne, passé en paramètre pour rendre la capacité stateless
    chain: List[Dict[str, Any]] = Field([], description="The current state of the immutable log chain.")
    # Paramètres pour l'action 'append'
    message_payload: Optional[Dict[str, Any]] = Field(None, description="The JSON-serializable message to append.")

class ChainedLogEntry(BaseModel):
    timestamp: float
    message_payload: Dict[str, Any]
    hash: str
    previous_hash: str

class AppendResult(BaseModel):
    new_entry: ChainedLogEntry
    updated_chain: List[ChainedLogEntry]

class VerifyResult(BaseModel):
    is_integrity_valid: bool
    first_tampered_index: Optional[int] = None

class ImmutableLogResult(BaseModel):
    action_performed: str
    result: Any # AppendResult or VerifyResult

class ImmutableLogCapability(ExecutableCapability):
    """
    Capacité stateless pour créer et vérifier des journaux immuables (hash chains).
    L'état de la chaîne doit être géré par l'appelant (ex: ZDM).
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "security.immutable_log_manager",
            "name": "Immutable Log Manager",
            "version": "2.1.0",
            "description": "Statelessly appends to and verifies immutable, hash-chained logs.",
            "dependencies": ["pydantic"],
            "input_schema": ImmutableLogParams.model_json_schema(),
            "output_schema": ImmutableLogResult.model_json_schema()
        }

    def _hash_entry(self, timestamp: float, message: Dict[str, Any], prev_hash: str) -> str:
        content = {
            "timestamp": timestamp,
            "message_payload": message,
            "previous_hash": prev_hash
        }
        content_string = json.dumps(content, sort_keys=True).encode()
        return hashlib.sha256(content_string).hexdigest()

    def _append(self, chain: List[Dict[str, Any]], message: Dict[str, Any]) -> AppendResult:
        previous_hash = chain[-1]["hash"] if chain else "0" * 64
        timestamp = time.time()
        
        current_hash = self._hash_entry(timestamp, message, previous_hash)
        
        new_entry = ChainedLogEntry(
            timestamp=timestamp,
            message_payload=message,
            hash=current_hash,
            previous_hash=previous_hash
        )
        
        updated_chain_data = chain + [new_entry.model_dump()]
        updated_chain = [ChainedLogEntry(**e) for e in updated_chain_data]
        
        return AppendResult(new_entry=new_entry, updated_chain=updated_chain)

    def _verify(self, chain: List[Dict[str, Any]]) -> VerifyResult:
        previous_hash = "0" * 64
        for i, entry_data in enumerate(chain):
            entry = ChainedLogEntry(**entry_data)
            expected_hash = self._hash_entry(entry.timestamp, entry.message_payload, previous_hash)
            
            if expected_hash != entry.hash or entry.previous_hash != previous_hash:
                return VerifyResult(is_integrity_valid=False, first_tampered_index=i)
            
            previous_hash = entry.hash
        
        return VerifyResult(is_integrity_valid=True)

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = ImmutableLogParams(**params)
        
        if p.action == "append":
            if p.message_payload is None:
                raise ValueError("'message_payload' is required for append action.")
            action_result = self._append(p.chain, p.message_payload)
        
        elif p.action == "verify":
            action_result = self._verify(p.chain)
        
        else:
            raise ValueError(f"Unknown action: {p.action}")

        result = ImmutableLogResult(action_performed=p.action, result=action_result)
        return result.model_dump()
