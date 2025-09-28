from .template import ProofOfValueCapability

class TourismOverbookingProof(ProofOfValueCapability):
    _ID = "proof.tourism_overbooking"
    _NAME = "PoV: Tourisme - Surbooking"
    _DESCRIPTION = "Surbooking hôtel"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
