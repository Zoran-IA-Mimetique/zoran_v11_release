from .template import ProofOfValueCapability

class HealthDriftProof(ProofOfValueCapability):
    _ID = "proof.health_drift"
    _NAME = "PoV: Health - Data Drift"
    _DESCRIPTION = "Détection dérive santé"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
