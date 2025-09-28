import hashlib
import time
import json
from typing import Dict, Any, List
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class HashChainParams(BaseModel):
    events: conlist(Dict[str, Any], min_length=1)

class ChainedEntry(BaseModel):
    event_payload: Dict[str, Any]
    hash: str
    previous_hash: str
    timestamp: float

class HashChainResult(BaseModel):
    chain: List[ChainedEntry]
    final_hash: str

class HashChainCapability(ExecutableCapability):
    """
    Construit une chaîne de hachage immuable (log inviolable) à partir d'une série d'événements.
    Ceci est une version plugin du `SecureLogger` du noyau.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "security.hash_chain_builder",
            "name": "Hash Chain Builder",
            "version": "2.0.0",
            "description": "Builds an immutable hash chain to trace events.",
            "dependencies": ["pydantic"],
            "input_schema": HashChainParams.model_json_schema(),
            "output_schema": HashChainResult.model_json_schema()
        }
        
    def _hash_entry(self, timestamp: float, event: Dict[str, Any], prev_hash: str) -> str:
        """Crée le contenu canonique d'une entrée et le hache."""
        content = {
            "timestamp": timestamp,
            "event_payload": event,
            "previous_hash": prev_hash
        }
        content_string = json.dumps(content, sort_keys=True).encode()
        return hashlib.sha256(content_string).hexdigest()

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = HashChainParams(**params)
        
        chain: List[ChainedEntry] = []
        previous_hash = "0" * 64

        for event_payload in p.events:
            timestamp = time.time()
            current_hash = self._hash_entry(timestamp, event_payload, previous_hash)
            chain.append(ChainedEntry(
                event_payload=event_payload,
                hash=current_hash,
                previous_hash=previous_hash,
                timestamp=timestamp
            ))
            previous_hash = current_hash
            
        result = HashChainResult(chain=chain, final_hash=previous_hash)
        return result.model_dump()
