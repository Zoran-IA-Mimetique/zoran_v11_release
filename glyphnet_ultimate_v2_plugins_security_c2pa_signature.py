import hashlib
import json
import time
import os
from typing import Dict, Any, Literal
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class C2PASignatureParams(BaseModel):
    artifact_path: str = Field(description="Path to the digital asset (file) to sign.")
    signer_id: str = Field(description="Identifier for the signing entity (e.g., 'zoran-labs-inc').")
    signature_algorithm: Literal["sha256", "sha512"] = Field("sha512")

class C2PAManifest(BaseModel):
    title: str = "C2PA Simplified Manifest"
    alg: str
    manifest_hash: str
    signature: str
    claims: Dict[str, Any]

class C2PASignatureCapability(ExecutableCapability):
    """
    Crée un manifeste signé pour un actif numérique, inspiré par la norme C2PA
    (Coalition for Content Provenance and Authenticity).
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "security.c2pa_simplified_manifest",
            "name": "C2PA-like Signed Manifest Generator",
            "version": "1.0.0-alpha",
            "description": "Creates a signed manifest for a digital asset, inspired by the C2PA standard.",
            "dependencies": ["pydantic"],
            "input_schema": C2PASignatureParams.model_json_schema(),
            "output_schema": C2PAManifest.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = C2PASignatureParams(**params)

        if not os.path.isfile(p.artifact_path):
            raise ValueError(f"Artifact not found at path: {p.artifact_path}")

        # 1. Calculer le hash de l'artefact
        with open(p.artifact_path, "rb") as f:
            artifact_data = f.read()
        artifact_hash = hashlib.sha256(artifact_data).hexdigest()

        # 2. Créer les "claims" (affirmations) du manifeste
        claims = {
            "data": {
                "hash": artifact_hash,
                "alg": "sha256"
            },
            "actions": [{
                "action": "c2pa.created",
                "when": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "digitalSourceType": "created-by-glyphnet-capability"
            }],
            "signatureInfo": {
                "issuer": p.signer_id
            }
        }
        
        # 3. Créer et signer le manifeste
        manifest_to_sign = {
            "title": "C2PA Simplified Manifest",
            "alg": p.signature_algorithm,
            "claims": claims
        }
        manifest_string = json.dumps(manifest_to_sign, sort_keys=True, separators=(',', ':')).encode()
        
        if p.signature_algorithm == "sha512":
            manifest_hash = hashlib.sha512(manifest_string).hexdigest()
        else: # sha256
            manifest_hash = hashlib.sha256(manifest_string).hexdigest()

        # Dans une vraie implémentation, la signature serait asymétrique (ex: PQC).
        # Ici, on simule une signature HMAC en utilisant le hash comme clé.
        signature = hashlib.sha512((manifest_hash + "secret-key-simulation").encode()).hexdigest()

        result = C2PAManifest(
            **manifest_to_sign,
            manifest_hash=manifest_hash,
            signature=signature
        )
        return result.model_dump()
