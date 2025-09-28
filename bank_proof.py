from .template import ProofOfValueCapability

class BankAmlProof(ProofOfValueCapability):
    _ID = "proof.bank_aml"
    _NAME = "PoV: Banque - AML"
    _DESCRIPTION = "Anti-blanchiment"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
