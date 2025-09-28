import ssl
import os
from typing import Dict, Any
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class SpiffeMTLSParams(BaseModel):
    cert_file_path: str = Field(description="Path to the certificate file (SVID).")
    key_file_path: str = Field(description="Path to the private key file.")
    ca_bundle_path: str = Field(description="Path to the CA bundle file for validating peers (Trust Bundle).")

class SpiffeMTLSResult(BaseModel):
    context_created: bool
    ssl_protocol: str
    error_message: Optional[str] = None

class SpiffeMTLSCapability(ExecutableCapability):
    """
    Crée un contexte SSL pour une communication mTLS, suivant les principes de SPIFFE.
    Cette capacité ne réalise pas la communication, mais prépare l'objet de contexte sécurisé.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "security.spiffe_mtls_context_builder",
            "name": "SPIFFE mTLS Context Builder",
            "version": "1.0.0-alpha",
            "description": "Creates a Python SSL context for mTLS communication, as used in SPIFFE.",
            "dependencies": ["pydantic"],
            "input_schema": SpiffeMTLSParams.model_json_schema(),
            "output_schema": SpiffeMTLSResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = SpiffeMTLSParams(**params)
        
        for path in [p.cert_file_path, p.key_file_path, p.ca_bundle_path]:
            if not os.path.isfile(path):
                raise ValueError(f"Required file not found at path: {path}")

        try:
            # Créer un contexte pour le côté serveur d'une connexion mTLS
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=p.ca_bundle_path)
            # Charger le certificat et la clé du serveur (son SVID)
            context.load_cert_chain(certfile=p.cert_file_path, keyfile=p.key_file_path)
            # Exiger que le client présente un certificat valide signé par notre CA
            context.verify_mode = ssl.CERT_REQUIRED
            
            result = SpiffeMTLSResult(
                context_created=True,
                ssl_protocol=context.protocol.name
            )
        except ssl.SSLError as e:
            result = SpiffeMTLSResult(
                context_created=False,
                ssl_protocol="N/A",
                error_message=f"SSL Error: {e}"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to create SSL context: {e}")
            
        # NOTE: Le contexte SSL lui-même n'est pas sérialisable en JSON.
        # Cette capacité est donc plus une "action" qu'une "transformation de données".
        # Le résultat atteste que la création a réussi.
        return result.model_dump()
