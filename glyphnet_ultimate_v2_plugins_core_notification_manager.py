import datetime
from typing import Dict, Any, List, Literal, Optional
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class Notification(BaseModel):
    recipient: str
    message: str
    timestamp_utc: str

class NotificationState(BaseModel):
    sent_notifications: List[Notification] = []

class NotificationManagerParams(BaseModel):
    action: Literal["send", "list"]
    current_state: NotificationState
    recipient: Optional[str] = None
    message: Optional[str] = None

class NotificationManagerResult(BaseModel):
    action_performed: str
    updated_state: NotificationState
    result: Any

class NotificationManagerCapability(ExecutableCapability):
    """
    Gère l'envoi (simulé) et la journalisation de notifications de manière stateless.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.stateless_notification_manager",
            "name": "Stateless Notification Manager",
            "version": "2.0.0",
            "description": "Manages sending and logging notifications statelessly.",
            "dependencies": ["pydantic"],
            "input_schema": NotificationManagerParams.model_json_schema(),
            "output_schema": NotificationManagerResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = NotificationManagerParams(**params)
        updated_state = p.current_state.copy(deep=True)
        action_result = None

        if p.action == "send":
            if not all([p.recipient, p.message]):
                raise ValueError("'recipient' and 'message' are required for 'send' action.")
            
            notif = Notification(
                recipient=p.recipient,
                message=p.message,
                timestamp_utc=datetime.datetime.utcnow().isoformat() + "Z"
            )
            # Dans une vraie implémentation, un side effect aurait lieu ici (appel API, email, etc.)
            # Ici, on se contente de l'ajouter au log.
            updated_state.sent_notifications.append(notif)
            action_result = notif

        elif p.action == "list":
            action_result = updated_state.sent_notifications

        result = NotificationManagerResult(
            action_performed=p.action,
            updated_state=updated_state,
            result=action_result
        )
        return result.model_dump()
