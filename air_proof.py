from .template import ProofOfValueCapability

class AirNoFlyProof(ProofOfValueCapability):
    _ID = "proof.air_no_fly_zone"
    _NAME = "PoV: Aérien - No Fly Zone"
    _DESCRIPTION = "Violation zone"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
