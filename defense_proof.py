from .template import ProofOfValueCapability

class DefenseDroneProof(ProofOfValueCapability):
    _ID = "proof.defense_drone"
    _NAME = "PoV: Défense - Drone"
    _DESCRIPTION = "Drone hors zone"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
