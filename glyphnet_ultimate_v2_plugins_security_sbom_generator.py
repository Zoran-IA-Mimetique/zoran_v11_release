import hashlib
import os
from typing import Dict, Any, List
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class SBOMParams(BaseModel):
    path_to_scan: str = Field(description="Directory path to scan for generating the SBOM.")
    hash_algorithm: str = Field("sha256", description="Hashing algorithm to use.")

class SBOMEntry(BaseModel):
    file_path: str
    hash: str

class SBOMResult(BaseModel):
    sbom_format: str = "simple-hash-list"
    file_count: int
    components: List[SBOMEntry]

class SBOMGeneratorCapability(ExecutableCapability):
    """
    Génère un SBOM (Software Bill of Materials) simple en listant les fichiers
    d'un répertoire et leur hash.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "security.simple_sbom_generator",
            "name": "Simple SBOM Generator",
            "version": "2.0.0",
            "description": "Generates a simple file-hash SBOM for a given directory.",
            "dependencies": ["pydantic"],
            "input_schema": SBOMParams.model_json_schema(),
            "output_schema": SBOMResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = SBOMParams(**params)
        
        if not os.path.isdir(p.path_to_scan):
            raise ValueError(f"Path not found or is not a directory: {p.path_to_scan}")

        if p.hash_algorithm != "sha256":
            raise ValueError("Only 'sha256' is supported in this version.")

        sbom_components: List[SBOMEntry] = []
        for root, _, files in os.walk(p.path_to_scan):
            for filename in files:
                full_path = os.path.join(root, filename)
                try:
                    with open(full_path, "rb") as f:
                        file_content = f.read()
                        file_hash = hashlib.sha256(file_content).hexdigest()
                    sbom_components.append(SBOMEntry(
                        file_path=os.path.relpath(full_path, p.path_to_scan),
                        hash=file_hash
                    ))
                except IOError:
                    # Ignorer les fichiers qui ne peuvent pas être lus
                    continue
        
        result = SBOMResult(file_count=len(sbom_components), components=sbom_components)
        return result.model_dump()
