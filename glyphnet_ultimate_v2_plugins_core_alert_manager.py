import datetime
import uuid
from typing import Dict, Any, List, Literal, Optional
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class Alert(BaseModel):
    alert_id: str
    message: str
    severity: Literal["info", "medium", "high", "critical"]
    timestamp_utc: str

class AlertState(BaseModel):
    active_alerts: List[Alert] = []

class AlertManagerParams(BaseModel):
    action: Literal["trigger", "list", "clear"]
    current_state: AlertState
    message: Optional[str] = None
    severity: Literal["info", "medium", "high", "critical"] = "medium"

class AlertManagerResult(BaseModel):
    action_performed: str
    updated_state: AlertState
    result: Any

class AlertManagerCapability(ExecutableCapability):
    """
    Gère un système d'alertes de manière stateless.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.stateless_alert_manager",
            "name": "Stateless Alert Manager",
            "version": "2.0.0",
            "description": "Manages a list of alerts statelessly.",
            "dependencies": ["pydantic"],
            "input_schema": AlertManagerParams.model_json_schema(),
            "output_schema": AlertManagerResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = AlertManagerParams(**params)
        updated_state = p.current_state.copy(deep=True)
        action_result = None

        if p.action == "trigger":
            if not p.message:
                raise ValueError("'message' is required for 'trigger' action.")
            
            alert = Alert(
                alert_id=f"alert_{uuid.uuid4().hex}",
                message=p.message,
                severity=p.severity,
                timestamp_utc=datetime.datetime.utcnow().isoformat() + "Z"
            )
            updated_state.active_alerts.append(alert)
            action_result = alert
        
        elif p.action == "list":
            action_result = updated_state.active_alerts
            
        elif p.action == "clear":
            updated_state.active_alerts.clear()
            action_result = {"status": "cleared"}

        result = AlertManagerResult(
            action_performed=p.action,
            updated_state=updated_state,
            result=action_result
        )
        return result.model_dump()
