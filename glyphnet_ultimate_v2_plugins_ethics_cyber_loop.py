import time
import hashlib
import json
from typing import Dict, Any, List
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class CyberLoopParams(BaseModel):
    events: conlist(str, min_length=1)

class LogEntry(BaseModel):
    event: str
    hash: str
    previous_hash: str
    timestamp: float

class CyberLoopResult(BaseModel):
    secure_log: List[LogEntry]
    final_chain_hash: str

class CyberLoopCapability(ExecutableCapability):
    """
    Capacité construisant une chaîne de hachage immuable pour un journal d'événements.
    Similaire au `SecureLogger` du noyau, mais encapsulé comme une capacité exécutable.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "ethics.immutable_log_generator",
            "name": "Immutable Log Generator",
            "version": "2.0.0",
            "description": "Builds a secure, hash-chained log from a list of events.",
            "dependencies": ["pydantic"],
            "input_schema": CyberLoopParams.model_json_schema(),
            "output_schema": CyberLoopResult.model_json_schema()
        }

    def _hash_entry_content(self, timestamp: float, event: str, previous_hash: str) -> str:
        """Crée une représentation canonique et hache le contenu."""
        content = {
            "timestamp": timestamp,
            "event": event,
            "previous_hash": previous_hash
        }
        # Utiliser json.dumps avec sort_keys pour un hash déterministe
        entry_string = json.dumps(content, sort_keys=True).encode()
        return hashlib.sha256(entry_string).hexdigest()

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Construit la chaîne de hachage."""
        p = CyberLoopParams(**params)
        
        log: List[LogEntry] = []
        previous_hash = "0" * 64
        
        for event_str in p.events:
            timestamp = time.time()
            current_hash = self._hash_entry_content(timestamp, event_str, previous_hash)
            
            log.append(LogEntry(
                event=event_str,
                hash=current_hash,
                previous_hash=previous_hash,
                timestamp=timestamp
            ))
            previous_hash = current_hash
            
        result = CyberLoopResult(
            secure_log=log,
            final_chain_hash=previous_hash
        )
        return result.model_dump()
