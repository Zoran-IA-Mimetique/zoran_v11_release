import datetime
import uuid
from typing import Dict, Any, Literal
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class PlaybookAlertsParams(BaseModel):
    event_name: str
    event_details: Dict[str, Any]
    severity: Literal["info", "low", "medium", "high", "critical"] = "medium"

class Alert(BaseModel):
    alert_id: str
    event_name: str
    severity: str
    timestamp_utc: str
    recommended_action: str
    details: Dict[str, Any]

class PlaybookAlertsCapability(ExecutableCapability):
    """
    Génère une alerte structurée basée sur un événement et sa sévérité,
    en suivant un playbook de réponse simple.
    """
    # Ce playbook pourrait être chargé depuis une configuration externe.
    RESPONSE_PLAYBOOK = {
        "info": "log_and_monitor",
        "low": "log_and_monitor",
        "medium": "investigate_within_24h",
        "high": "escalate_to_level_2_support",
        "critical": "trigger_incident_response_protocol"
    }
    
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "security.playbook_alert_trigger",
            "name": "Playbook-based Alert Trigger",
            "version": "2.0.0",
            "description": "Triggers a structured alert according to a predefined response playbook.",
            "dependencies": ["pydantic"],
            "input_schema": PlaybookAlertsParams.model_json_schema(),
            "output_schema": Alert.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = PlaybookAlertsParams(**params)

        recommended_action = self.RESPONSE_PLAYBOOK.get(p.severity, "log_and_monitor")
        
        alert = Alert(
            alert_id=f"alert_{uuid.uuid4().hex}",
            event_name=p.event_name,
            severity=p.severity,
            timestamp_utc=datetime.datetime.utcnow().isoformat() + "Z",
            recommended_action=recommended_action,
            details=p.event_details
        )
        
        # Dans une vraie implémentation, cette capacité pourrait également envoyer
        # l'alerte à un système externe (SIEM, PagerDuty, Slack, etc.).
        # Pour l'instant, elle retourne simplement l'objet d'alerte.

        return alert.model_dump()
