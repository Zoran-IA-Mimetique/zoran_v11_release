import os
import hashlib
from typing import Dict, Any, List
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class ForensicsAuditParams(BaseModel):
    directory_path: str = Field(description="The directory to audit.")
    hash_algorithm: str = Field("sha256", description="The hashing algorithm to use.")

class FileForensicRecord(BaseModel):
    relative_path: str
    hash: str
    size_bytes: int

class ForensicsAuditResult(BaseModel):
    files_scanned: int
    directory_hash: str = Field(description="A cumulative hash of all file hashes, providing a single integrity value for the directory.")
    report: List[FileForensicRecord]

class ForensicsAuditCapability(ExecutableCapability):
    """
    Réalise un audit forensique simple d'un répertoire en calculant
    les empreintes de tous les fichiers et une empreinte globale du répertoire.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "security.forensics_directory_audit",
            "name": "Forensic Directory Audit",
            "version": "2.0.0",
            "description": "Performs a simple forensic audit of a directory by hashing all its files.",
            "dependencies": ["pydantic"],
            "input_schema": ForensicsAuditParams.model_json_schema(),
            "output_schema": ForensicsAuditResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = ForensicsAuditParams(**params)

        if not os.path.isdir(p.directory_path):
            raise ValueError(f"Path not found or is not a directory: {p.directory_path}")

        if p.hash_algorithm != "sha256":
            raise ValueError("Only 'sha256' is supported in this version.")

        report: List[FileForensicRecord] = []
        all_hashes = []

        for root, _, files in os.walk(p.directory_path):
            for filename in sorted(files): # Trier pour un hash de répertoire déterministe
                full_path = os.path.join(root, filename)
                try:
                    with open(full_path, "rb") as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()
                    
                    file_size = os.path.getsize(full_path)
                    relative_path = os.path.relpath(full_path, p.directory_path)
                    
                    report.append(FileForensicRecord(
                        relative_path=relative_path,
                        hash=file_hash,
                        size_bytes=file_size
                    ))
                    all_hashes.append(file_hash)
                except (IOError, OSError):
                    continue
        
        # Calculer un hash global pour le répertoire en hachant la chaîne des hashs triés
        directory_hash = hashlib.sha256("".join(sorted(all_hashes)).encode()).hexdigest()

        result = ForensicsAuditResult(
            files_scanned=len(report),
            directory_hash=directory_hash,
            report=report
        )
        return result.model_dump()
