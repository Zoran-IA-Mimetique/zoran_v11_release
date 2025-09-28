from typing import Dict, Any
from pantic import BaseModel, Field

class ProofOfValueCapability:
    _ID = "proof.abstract"
    _NAME = "Abstract Proof"
    _DESCRIPTION = "Base template"

    def metadata(self) -> Dict[str, Any]:
        return {
            "id": self._ID,
            "name": self._NAME,
            "description": self._DESCRIPTION,
            "version": "1.0.0"
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        success, msg, details = self._run_proof_logic()
        return {"success": success, "message": msg, "details": details}

    def _run_proof_logic(self) -> (bool, str, Dict[str, Any]):
        raise NotImplementedError
