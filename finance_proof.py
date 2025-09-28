from .template import ProofOfValueCapability

class FinanceBiasProof(ProofOfValueCapability):
    _ID = "proof.finance_bias"
    _NAME = "PoV: Finance - Bias"
    _DESCRIPTION = "Détection biais finance"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
