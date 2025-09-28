import hashlib
import time
from typing import Dict, Any, List, Literal, Optional
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class Evidence(BaseModel):
    claim: str
    source: str
    content_hash: str
    timestamp: float

class EvidenceState(BaseModel):
    evidence_log: List[Evidence] = []

class EvidenceManagerParams(BaseModel):
    action: Literal["add", "list"]
    current_state: EvidenceState
    claim: Optional[str] = None
    source: Optional[str] = None
    content: Optional[str] = None

class EvidenceManagerResult(BaseModel):
    action_performed: str
    updated_state: EvidenceState
    result: Any

class EvidenceManagerCapability(ExecutableCapability):
    """
    Gère une collection de preuves (claims) de manière stateless.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.stateless_evidence_manager",
            "name": "Stateless Evidence Manager",
            "version": "2.0.0",
            "description": "Manages a collection of evidence records statelessly.",
            "dependencies": ["pydantic"],
            "input_schema": EvidenceManagerParams.model_json_schema(),
            "output_schema": EvidenceManagerResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = EvidenceManagerParams(**params)
        updated_state = p.current_state.copy(deep=True)
        action_result = None

        if p.action == "add":
            if not all([p.claim, p.source, p.content]):
                raise ValueError("'claim', 'source', and 'content' are required for 'add' action.")
            
            entry = Evidence(
                claim=p.claim,
                source=p.source,
                content_hash=hashlib.sha256(p.content.encode("utf-8")).hexdigest(),
                timestamp=time.time()
            )
            updated_state.evidence_log.append(entry)
            action_result = entry

        elif p.action == "list":
            action_result = updated_state.evidence_log

        result = EvidenceManagerResult(
            action_performed=p.action,
            updated_state=updated_state,
            result=action_result
        )
        return result.model_dump()
