from .template import ProofOfValueCapability

class NgoAllocationProof(ProofOfValueCapability):
    _ID = "proof.ngo_allocation"
    _NAME = "PoV: ONG - Allocation"
    _DESCRIPTION = "Allocation transparente"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
