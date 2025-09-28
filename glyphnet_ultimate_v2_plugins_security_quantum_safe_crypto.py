from typing import Dict, Any, Literal, Tuple
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

# Tente d'importer oqs, mais ne lève une erreur qu'à l'exécution si nécessaire.
try:
    from oqs import Signature
    OQS_AVAILABLE = True
except ImportError:
    OQS_AVAILABLE = False

class QuantumSafeCryptoParams(BaseModel):
    action: Literal["generate_keypair", "sign", "verify"]
    algorithm: str = Field("Dilithium3", description="Post-quantum signature algorithm to use.")
    # Paramètres optionnels
    private_key: Optional[bytes] = None
    public_key: Optional[bytes] = None
    message: Optional[bytes] = None
    signature: Optional[bytes] = None

class KeyPair(BaseModel):
    public_key: bytes
    private_key: bytes

class SignResult(BaseModel):
    signature: bytes

class VerifyResult(BaseModel):
    is_valid: bool

class QuantumSafeCryptoResult(BaseModel):
    action_performed: str
    result: Any

class QuantumSafeCryptoCapability(ExecutableCapability):
    """
    Wrapper pour la bibliothèque liboqs, fournissant des capacités de
    cryptographie post-quantique. Nécessite `oqs-python` installé.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "security.quantum_safe_crypto",
            "name": "Post-Quantum Cryptography (liboqs)",
            "version": "2.0.0",
            "description": "Provides PQC key generation, signing, and verification using liboqs.",
            "dependencies": ["oqs-python", "pydantic"],
            "input_schema": QuantumSafeCryptoParams.model_json_schema(),
            "output_schema": QuantumSafeCryptoResult.model_json_schema()
        }
        
    def _check_oqs_installed(self):
        if not OQS_AVAILABLE:
            raise RuntimeError("The 'oqs-python' library is not installed. Please run 'pip install oqs'.")

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        self._check_oqs_installed()
        p = QuantumSafeCryptoParams(**params)

        try:
            if p.action == "generate_keypair":
                sig = Signature(p.algorithm)
                public_key = sig.generate_keypair()
                private_key = sig.export_secret_key()
                action_result = KeyPair(public_key=public_key, private_key=private_key)
            
            elif p.action == "sign":
                if p.private_key is None or p.message is None:
                    raise ValueError("'private_key' and 'message' are required for signing.")
                sig = Signature(p.algorithm, secret_key=p.private_key)
                signature = sig.sign(p.message)
                action_result = SignResult(signature=signature)
            
            elif p.action == "verify":
                if p.public_key is None or p.message is None or p.signature is None:
                    raise ValueError("'public_key', 'message', and 'signature' are required for verification.")
                sig = Signature(p.algorithm)
                is_valid = sig.verify(p.message, p.signature, p.public_key)
                action_result = VerifyResult(is_valid=is_valid)

            else:
                raise ValueError(f"Unknown action: {p.action}")

        except Exception as e:
            # Capturer les erreurs potentielles de liboqs (ex: mauvais format de clé)
            raise RuntimeError(f"OQS operation failed for algorithm '{p.algorithm}': {e}")

        result = QuantumSafeCryptoResult(action_performed=p.action, result=action_result)
        return result.model_dump(mode='json') # `bytes` n'est pas directement sérialisable en JSON, mode='json' le gère
