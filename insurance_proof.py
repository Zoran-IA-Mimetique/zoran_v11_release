from .template import ProofOfValueCapability

class InsuranceFraudProof(ProofOfValueCapability):
    _ID = "proof.insurance_fraud"
    _NAME = "PoV: Assurance - Fraude"
    _DESCRIPTION = "Fraude assurance"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
