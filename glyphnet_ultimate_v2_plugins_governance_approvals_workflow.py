import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from glyphnet_ultimate_v2.engines.capabilities import ExecutableCapability

class Approval(BaseModel):
    approver_id: str
    timestamp_utc: str

class ApprovalsWorkflowParams(BaseModel):
    # L'état est passé en paramètre pour rendre la capacité stateless
    required_approvals: int = Field(2, gt=0)
    current_approvals: List[Approval] = []
    # L'action est d'approuver ou de vérifier
    action: Literal["approve", "check_status"]
    approver_id: Optional[str] = None # Requis pour l'action 'approve'

class ApprovalStatus(BaseModel):
    is_fully_approved: bool
    required_count: int
    current_count: int
    approvers: List[str]

class ApprovalsWorkflowResult(BaseModel):
    status: ApprovalStatus
    updated_approvals: List[Approval]

class ApprovalsWorkflowCapability(ExecutableCapability):
    """
    Gère un workflow d'approbation stateless où l'état des approbations
    est passé à chaque appel.
    """
    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "governance.approvals_workflow",
            "name": "Stateless Approvals Workflow",
            "version": "2.0.0",
            "description": "Manages a multi-signature approval workflow statelessly.",
            "dependencies": ["pydantic"],
            "input_schema": ApprovalsWorkflowParams.model_json_schema(),
            "output_schema": ApprovalsWorkflowResult.model_json_schema()
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        p = ApprovalsWorkflowParams(**params)
        
        updated_approvals = p.current_approvals.copy()

        if p.action == "approve":
            if not p.approver_id:
                raise ValueError("'approver_id' is required for the 'approve' action.")
            
            # Empêcher un approbateur de voter deux fois
            if any(app.approver_id == p.approver_id for app in updated_approvals):
                pass # Ou lever une erreur, selon la politique souhaitée. Ici on l'ignore.
            else:
                updated_approvals.append(Approval(
                    approver_id=p.approver_id,
                    timestamp_utc=datetime.datetime.utcnow().isoformat() + "Z"
                ))
        
        current_approvers_list = [app.approver_id for app in updated_approvals]
        status = ApprovalStatus(
            is_fully_approved=len(updated_approvals) >= p.required_approvals,
            required_count=p.required_approvals,
            current_count=len(updated_approvals),
            approvers=current_approvers_list
        )

        result = ApprovalsWorkflowResult(status=status, updated_approvals=updated_approvals)
        return result.model_dump()
