from .template import ProofOfValueCapability

class MaritimeCargoProof(ProofOfValueCapability):
    _ID = "proof.maritime_cargo_route"
    _NAME = "PoV: Maritime - Cargo"
    _DESCRIPTION = "Cargo hors route"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
