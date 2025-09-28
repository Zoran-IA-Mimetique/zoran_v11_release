import hashlib
import json
import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class SLSAProvenanceParams(BaseModel):
    builder_id: str = Field("glyphnet-builder-v1", description="Identifier for the build system.")
    build_trigger_id: str = Field(description="Identifier for the event that triggered the build (e.g., git commit hash).")
    artifact_paths: conlist(str, min_length=1)

class ArtifactDigest(BaseModel):
    file_path: str
    sha256: str

class SLSAProvenanceResult(BaseModel):
    provenance_statement: Dict[str, Any]
    json_representation: str

class SLSAProvenanceCapability(ExecutableCapability):
    """
    Génère un document de provenance simple, inspiré du framework SLSA,
    pour attester de l'origine d'un ensemble d'artefacts.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "security.slsa_provenance_generator",
            "name": "SLSA-like Provenance Generator",
            "version": "1.0.0-alpha",
            "description": "Generates a simple SLSA-like provenance statement for build artifacts.",
            "dependencies": ["pydantic"],
            "input_schema": SLSAProvenanceParams.model_json_schema(),
            "output_schema": SLSAProvenanceResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = SLSAProvenanceParams(**params)
        
        artifact_digests: List[ArtifactDigest] = []
        for path in p.artifact_paths:
            if not os.path.isfile(path):
                raise ValueError(f"Artifact path not found or is not a file: {path}")
            with open(path, "rb") as f:
                content = f.read()
                digest = hashlib.sha256(content).hexdigest()
            artifact_digests.append(ArtifactDigest(file_path=os.path.basename(path), sha256=digest))

        # Construction de la déclaration de provenance (structure simplifiée)
        provenance = {
            "_type": "https://in-toto.io/Statement/v0.1",
            "subject": [d.model_dump() for d in artifact_digests],
            "predicateType": "https://slsa.dev/provenance/v0.2",
            "predicate": {
                "builder": {"id": p.builder_id},
                "buildType": "glyphnet-custom-build",
                "invocation": {"trigger": p.build_trigger_id},
                "metadata": {"buildFinishedOn": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
            }
        }
        
        result = SLSAProvenanceResult(
            provenance_statement=provenance,
            json_representation=json.dumps(provenance, indent=2)
        )
        return result.model_dump()
