import time
from typing import Dict, Any, Literal, Optional, List
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class CacheEntry(BaseModel):
    value: Any
    expiry_timestamp: float

class CacheState(BaseModel):
    # Dictionnaire de CacheEntry
    entries: Dict[str, CacheEntry] = {}

class CacheManagerParams(BaseModel):
    action: Literal["put", "get", "invalidate", "clear"]
    # État stateless
    current_cache: CacheState
    # Paramètres d'action
    key: Optional[str] = None
    value: Optional[Any] = None
    ttl_seconds: int = 60

class CacheGetResult(BaseModel):
    is_hit: bool
    value: Optional[Any] = None

class CacheManagerResult(BaseModel):
    action_performed: str
    updated_cache: CacheState
    result: Any

class CacheManagerCapability(ExecutableCapability):
    """
    Capacité de gestion de cache stateless (en mémoire), avec support du TTL.
    L'état du cache est passé en paramètre à chaque appel.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.stateless_cache_manager",
            "name": "Stateless Cache Manager",
            "version": "2.0.0",
            "description": "Provides stateless in-memory caching operations (put, get, invalidate).",
            "dependencies": ["pydantic"],
            "input_schema": CacheManagerParams.model_json_schema(),
            "output_schema": CacheManagerResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = CacheManagerParams(**params)
        
        # Nettoyer les entrées expirées avant toute opération
        current_time = time.time()
        active_entries = {
            k: v for k, v in p.current_cache.entries.items()
            if v.expiry_timestamp >= current_time
        }
        updated_cache_state = CacheState(entries=active_entries)
        action_result = None

        if p.action == "put":
            if p.key is None or p.value is None:
                raise ValueError("'key' and 'value' are required for 'put' action.")
            expiry = current_time + p.ttl_seconds
            updated_cache_state.entries[p.key] = CacheEntry(value=p.value, expiry_timestamp=expiry)
            action_result = {"status": "cached", "key": p.key, "expiry": expiry}

        elif p.action == "get":
            if p.key is None:
                raise ValueError("'key' is required for 'get' action.")
            entry = updated_cache_state.entries.get(p.key)
            if entry:
                action_result = CacheGetResult(is_hit=True, value=entry.value)
            else:
                action_result = CacheGetResult(is_hit=False)

        elif p.action == "invalidate":
            if p.key is None:
                raise ValueError("'key' is required for 'invalidate' action.")
            if p.key in updated_cache_state.entries:
                del updated_cache_state.entries[p.key]
                action_result = {"status": "invalidated", "key": p.key}
            else:
                action_result = {"status": "not_found", "key": p.key}

        elif p.action == "clear":
            updated_cache_state.entries.clear()
            action_result = {"status": "cleared"}

        else:
            raise ValueError(f"Unknown action: {p.action}")

        result = CacheManagerResult(
            action_performed=p.action,
            updated_cache=updated_cache_state,
            result=action_result
        )
        return result.model_dump()
