import json
from typing import Dict, Any, List
from pydantic import BaseModel, Field, ValidationError

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class VEXValidationParams(BaseModel):
    vex_document: Dict[str, Any] = Field(description="A VEX document parsed as a Python dictionary.")

class VEXValidationResult(BaseModel):
    is_valid: bool
    errors: List[str]

class VEXValidationCapability(ExecutableCapability):
    """
    Valide un document VEX (Vulnerability Exploitability eXchange) minimal
    contre un schéma Pydantic simple.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "security.vex_validator",
            "name": "VEX Document Validator",
            "version": "2.0.0",
            "description": "Validates a minimal VEX document structure.",
            "dependencies": ["pydantic"],
            "input_schema": VEXValidationParams.model_json_schema(),
            "output_schema": VEXValidationResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        
        # Définir le schéma attendu pour un document VEX simple
        class VEXProduct(BaseModel):
            product_id: str

        class VEXVulnerability(BaseModel):
            vulnerability_id: str

        class VEXStatement(BaseModel):
            status: Literal["not_affected", "affected", "fixed", "under_investigation"]
            justification: Optional[str] = None
        
        class MinimalVEX(BaseModel):
            product: VEXProduct
            vulnerability: VEXVulnerability
            statement: VEXStatement

        p = VEXValidationParams(**params)
        
        try:
            MinimalVEX(**p.vex_document)
            result = VEXValidationResult(is_valid=True, errors=[])
        except ValidationError as e:
            result = VEXValidationResult(is_valid=False, errors=e.errors())
        
        return result.model_dump()
