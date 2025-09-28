import hashlib
import json
from typing import Dict, Any, List, Literal
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class ValidationManagerParams(BaseModel):
    action: Literal["validate_schema", "validate_integrity"]
    document: Dict[str, Any]
    required_fields: Optional[conlist(str, min_length=1)] = None # for schema
    checksum_field: str = "sha256_checksum" # for integrity

class ValidationManagerResult(BaseModel):
    action_performed: str
    is_valid: bool
    details: Dict[str, Any]

class ValidationManagerCapability(ExecutableCapability):
    """
    Fournit des services de validation de documents (schéma et intégrité).
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "core.validation_manager",
            "name": "Document Validation Manager",
            "version": "2.0.0",
            "description": "Provides document schema and integrity validation services.",
            "dependencies": ["pydantic"],
            "input_schema": ValidationManagerParams.model_json_schema(),
            "output_schema": ValidationManagerResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = ValidationManagerParams(**params)
        
        if p.action == "validate_schema":
            if p.required_fields is None:
                raise ValueError("'required_fields' is required for 'validate_schema' action.")
            
            missing = [field for field in p.required_fields if field not in p.document]
            is_valid = len(missing) == 0
            details = {"missing_fields": missing}
            
        elif p.action == "validate_integrity":
            if p.checksum_field not in p.document:
                is_valid = False
                details = {"error": f"Checksum field '{p.checksum_field}' is missing."}
            else:
                checksum = p.document[p.checksum_field]
                payload = {k: v for k, v in p.document.items() if k != p.checksum_field}
                calculated_checksum = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
                is_valid = (calculated_checksum == checksum)
                details = {"expected_checksum": calculated_checksum, "provided_checksum": checksum}

        else:
            raise ValueError(f"Unknown action: {p.action}")
            
        return ValidationManagerResult(action_performed=p.action, is_valid=is_valid, details=details).model_dump()
