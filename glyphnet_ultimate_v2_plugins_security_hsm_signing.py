import hashlib
import os
from typing import Dict, Any, Literal, Optional
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class HSMSigningParams(BaseModel):
    action: Literal["sign", "verify"]
    message: str
    # La clé est passée pour rendre la capacité stateless
    secret_key_hex: str
    signature: Optional[str] = None

class SignResultHSM(BaseModel):
    signature: str

class VerifyResultHSM(BaseModel):
    is_valid: bool

class HSMSigningResult(BaseModel):
    action_performed: str
    result: Any # SignResultHSM or VerifyResultHSM

class HSMCapability(ExecutableCapability):
    """
    Simule la signature et la vérification de messages comme le ferait un
    Hardware Security Module (HSM), en utilisant une clé secrète symétrique (HMAC-like).
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "security.hsm_simulation",
            "name": "HSM Signing Simulation",
            "version": "2.0.0",
            "description": "Simulates message signing and verification using a secret key, as an HSM would.",
            "dependencies": ["pydantic"],
            "input_schema": HSMSigningParams.model_json_schema(),
            "output_schema": HSMSigningResult.model_json_schema()
        }
        
    def _compute_hmac(self, secret_key: bytes, message: str) -> str:
        """Helper for HMAC-like computation."""
        return hashlib.sha256(secret_key + message.encode("utf-8")).hexdigest()

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = HSMSigningParams(**params)
        
        try:
            secret_key = bytes.fromhex(p.secret_key_hex)
        except ValueError:
            raise ValueError("'secret_key_hex' is not a valid hex string.")

        if p.action == "sign":
            signature = self._compute_hmac(secret_key, p.message)
            action_result = SignResultHSM(signature=signature)
            
        elif p.action == "verify":
            if p.signature is None:
                raise ValueError("'signature' is required for verification.")
            expected_signature = self._compute_hmac(secret_key, p.message)
            action_result = VerifyResultHSM(is_valid=(expected_signature == p.signature))

        else:
            raise ValueError(f"Unknown action: {p.action}")

        result = HSMSigningResult(action_performed=p.action, result=action_result)
        return result.model_dump()
