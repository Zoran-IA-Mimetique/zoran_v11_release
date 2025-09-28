import uuid
import time
from typing import Dict, Any, List, Literal, Optional
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class Trace(BaseModel):
    trace_id: str
    actor: str
    action: str
    details: Dict[str, Any]
    timestamp: float

class TraceState(BaseModel):
    traces: Dict[str, Trace] = {}

class TraceabilityManagerParams(BaseModel):
    action: Literal["record", "get"]
    current_state: TraceState
    actor: Optional[str] = None
    action_name: Optional[str] = Field(None, alias="action")
    details: Optional[Dict[str, Any]] = None
    trace_id: Optional[str] = None

class TraceabilityManagerResult(BaseModel):
    action_performed: str
    updated_state: TraceState
    result: Any

class TraceabilityManagerCapability(ExecutableCapability):
    """
    Gère un journal de traçabilité des actions de manière stateless.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.stateless_traceability_manager",
            "name": "Stateless Traceability Manager",
            "version": "2.0.0",
            "description": "Manages an action traceability log statelessly.",
            "dependencies": ["pydantic"],
            "input_schema": TraceabilityManagerParams.model_json_schema(),
            "output_schema": TraceabilityManagerResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = TraceabilityManagerParams(**params)
        updated_state = p.current_state.copy(deep=True)
        action_result = None

        if p.action == "record":
            if not all([p.actor, p.action_name]):
                raise ValueError("'actor' and 'action_name' are required for 'record' action.")
            
            entry = Trace(
                trace_id=f"trace_{uuid.uuid4().hex}",
                actor=p.actor,
                action=p.action_name,
                details=p.details or {},
                timestamp=time.time()
            )
            updated_state.traces[entry.trace_id] = entry
            action_result = entry

        elif p.action == "get":
            if not p.trace_id:
                raise ValueError("'trace_id' is required for 'get' action.")
            action_result = updated_state.traces.get(p.trace_id)

        result = TraceabilityManagerResult(
            action_performed=p.action,
            updated_state=updated_state,
            result=action_result
        )
        return result.model_dump()
