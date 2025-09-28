import datetime
from typing import Dict, Any, List, Literal, Optional
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class LogEntry(BaseModel):
    timestamp_utc: str
    level: Literal["info", "warning", "error", "debug"]
    message: str

class LoggerState(BaseModel):
    logs: List[LogEntry] = []

class LoggerParams(BaseModel):
    action: Literal["log", "get"]
    current_state: LoggerState
    level: Optional[Literal["info", "warning", "error", "debug"]] = "info"
    message: Optional[str] = None
    filter_level: Optional[Literal["info", "warning", "error", "debug"]] = None

class LoggerResult(BaseModel):
    action_performed: str
    updated_state: LoggerState
    result: Any

class LoggerCapability(ExecutableCapability):
    """
    Gère une liste de logs structurés de manière stateless.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.stateless_logger",
            "name": "Stateless Logger",
            "version": "2.0.0",
            "description": "Manages a structured log list statelessly.",
            "dependencies": ["pydantic"],
            "input_schema": LoggerParams.model_json_schema(),
            "output_schema": LoggerResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = LoggerParams(**params)
        updated_state = p.current_state.copy(deep=True)
        action_result = None

        if p.action == "log":
            if p.message is None or p.level is None:
                raise ValueError("'message' and 'level' are required for 'log' action.")
            entry = LogEntry(
                timestamp_utc=datetime.datetime.utcnow().isoformat() + "Z",
                level=p.level,
                message=p.message
            )
            updated_state.logs.append(entry)
            action_result = entry

        elif p.action == "get":
            if p.filter_level:
                action_result = [log for log in updated_state.logs if log.level == p.filter_level]
            else:
                action_result = updated_state.logs

        result = LoggerResult(action_performed=p.action, updated_state=updated_state, result=action_result)
        return result.model_dump()
