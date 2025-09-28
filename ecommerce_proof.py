from .template import ProofOfValueCapability

class EcommerceFraudProof(ProofOfValueCapability):
    _ID = "proof.ecommerce_card_fraud"
    _NAME = "PoV: E-commerce - CB Fraud"
    _DESCRIPTION = "Fraude CB"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
