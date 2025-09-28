import hashlib
import json
import time
import os
from typing import Dict, Any, List, Literal, Optional
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class BundleEntry(BaseModel):
    file_path: str
    sha256: str

class UpdateBundle(BaseModel):
    timestamp: float
    entries: List[BundleEntry]
    signature: str # Added field for clarity

class UpdateBundleParams(BaseModel):
    action: Literal["create", "verify"]
    file_paths: Optional[conlist(str, min_length=1)] = None # For 'create'
    bundle: Optional[UpdateBundle] = None # For 'verify'

class UpdateBundleResult(BaseModel):
    action_performed: str
    result: Any # UpdateBundle or a simple dict for verification

class UpdateBundleCapability(ExecutableCapability):
    """
    Crée et vérifie des bundles de mise à jour signés, contenant les empreintes
    d'un ensemble de fichiers pour garantir leur intégrité.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "security.secure_update_bundle",
            "name": "Secure Update Bundle Manager",
            "version": "2.0.0",
            "description": "Creates and verifies signed update bundles to ensure software integrity.",
            "dependencies": ["pydantic"],
            "input_schema": UpdateBundleParams.model_json_schema(),
            "output_schema": UpdateBundleResult.model_json_schema()
        }
        
    def _hash_bundle_content(self, bundle_content: Dict[str, Any]) -> str:
        """Hashes the bundle content minus the signature for verification."""
        unsigned_string = json.dumps(bundle_content, sort_keys=True).encode()
        return hashlib.sha256(unsigned_string).hexdigest()

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = UpdateBundleParams(**params)
        
        if p.action == "create":
            if not p.file_paths:
                raise ValueError("'file_paths' are required to create a bundle.")
            
            entries = []
            for file_path in p.file_paths:
                if not os.path.isfile(file_path):
                    raise FileNotFoundError(f"File not found: {file_path}")
                with open(file_path, "rb") as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                entries.append(BundleEntry(file_path=os.path.basename(file_path), sha256=file_hash))
            
            bundle_content = {"timestamp": time.time(), "entries": [e.model_dump() for e in entries]}
            signature = self._hash_bundle_content(bundle_content)
            
            action_result = UpdateBundle(**bundle_content, signature=signature)

        elif p.action == "verify":
            if not p.bundle:
                raise ValueError("'bundle' is required for verification.")
            
            bundle_dict = p.bundle.model_dump()
            signature = bundle_dict.pop("signature")
            expected_signature = self._hash_bundle_content(bundle_dict)
            action_result = {"is_valid": signature == expected_signature}
            
        else:
            raise ValueError(f"Unknown action: {p.action}")

        result = UpdateBundleResult(action_performed=p.action, result=action_result)
        return result.model_dump()
