""" ZDM with Merkle-like log (minimal) """

import hashlib, json
from typing import Dict, Any, List
class ZDM:
    def __init__(self): self._state: Dict[str, Any] = {}; self._log: List[Dict[str, Any]] = []; self._root=None
    def commit(self, operation: str, payload: Dict[str, Any], metadata: Dict[str, Any] = None):
        self._state.update(payload); self._log.append({'op':operation,'payload':payload}); self._root=self._hash_log()
    def _hash_log(self): return hashlib.sha256(json.dumps(self._log, sort_keys=True).encode()).hexdigest()
    def get_current_state(self): return dict(self._state)
    def get_current_state_hash(self): return self._root
