import hashlib
import json
from typing import Dict, Any, Literal
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class SignatureManagerParams(BaseModel):
    action: Literal["sign", "verify"]
    document: Dict[str, Any]
    secret_key: str = Field(description="The secret key for HMAC-like signing.")
    signature: Optional[str] = None

class SignatureManagerResult(BaseModel):
    action_performed: str
    is_valid: Optional[bool] = None
    signature: Optional[str] = None

class SignatureManagerCapability(ExecutableCapability):
    """
    Signe et vérifie des documents JSON en utilisant un secret partagé (HMAC-SHA256).
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.symmetric_signature_manager",
            "name": "Symmetric Signature Manager",
            "version": "2.0.0",
            "description": "Signs and verifies JSON documents using a shared secret (HMAC-SHA256).",
            "dependencies": ["pydantic"],
            "input_schema": SignatureManagerParams.model_json_schema(),
            "output_schema": SignatureManagerResult.model_json_schema()
        }

    def _compute_signature(self, document: Dict[str, Any], secret: str) -> str:
        payload = json.dumps(document, sort_keys=True, separators=(',', ':')).encode("utf-8")
        return hashlib.sha256(secret.encode("utf-8") + payload).hexdigest()

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = SignatureManagerParams(**params)
        
        if p.action == "sign":
            signature = self._compute_signature(p.document, p.secret_key)
            return SignatureManagerResult(action_performed="sign", signature=signature).model_dump()
            
        elif p.action == "verify":
            if p.signature is None:
                raise ValueError("'signature' is required for 'verify' action.")
            expected_signature = self._compute_signature(p.document, p.secret_key)
            is_valid = (expected_signature == p.signature)
            return SignatureManagerResult(action_performed="verify", is_valid=is_valid).model_dump()
        
        raise ValueError(f"Unknown action: {p.action}")
