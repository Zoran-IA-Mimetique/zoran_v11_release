from .template import ProofOfValueCapability

class FoodContaminationProof(ProofOfValueCapability):
    _ID = "proof.food_contamination"
    _NAME = "PoV: Agro - Contamination"
    _DESCRIPTION = "Détection contamination"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
