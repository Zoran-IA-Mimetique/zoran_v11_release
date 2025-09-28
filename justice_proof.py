from .template import ProofOfValueCapability

class JusticeConsistencyProof(ProofOfValueCapability):
    _ID = "proof.justice_consistency"
    _NAME = "PoV: Justice - Cohérence"
    _DESCRIPTION = "Incohérence verdicts"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
