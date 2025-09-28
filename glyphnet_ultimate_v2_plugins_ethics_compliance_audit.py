from typing import Dict, Any, List, Set
from pydantic import BaseModel, Field, conlist

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class ComplianceAuditParams(BaseModel):
    declared_policies: Set[str]

class ComplianceAuditResult(BaseModel):
    is_compliant: bool
    missing_policies: List[str]
    checked_policies: List[str]
    extra_policies: List[str]

class ComplianceAuditCapability(ExecutableCapability):
    """
    Capacité d'audit de conformité qui vérifie une liste de politiques
    par rapport à un ensemble de politiques de base requises.
    """
    # Cet ensemble pourrait être chargé dynamiquement à partir d'une configuration externe.
    REQUIRED_BASE_POLICIES: Set[str] = {"data_protection", "human_oversight", "accountability"}

    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "ethics.compliance_policy_audit",
            "name": "Compliance Policy Audit",
            "version": "2.0.0",
            "description": "Audits a set of declared policies against a required baseline.",
            "dependencies": ["pydantic"],
            "input_schema": ComplianceAuditParams.model_json_schema(),
            "output_schema": ComplianceAuditResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute l'audit de politiques."""
        p = ComplianceAuditParams(**params)
        
        missing = self.REQUIRED_BASE_POLICIES - p.declared_policies
        # Politiques supplémentaires que l'utilisateur a déclarées au-delà du minimum requis
        extras = p.declared_policies - self.REQUIRED_BASE_POLICIES
        
        result = ComplianceAuditResult(
            is_compliant=len(missing) == 0,
            missing_policies=sorted(list(missing)),
            checked_policies=sorted(list(self.REQUIRED_BASE_POLICIES)),
            extra_policies=sorted(list(extras))
        )
        return result.model_dump()
