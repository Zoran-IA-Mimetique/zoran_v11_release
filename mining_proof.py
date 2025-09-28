from .template import ProofOfValueCapability

class MiningAccidentProof(ProofOfValueCapability):
    _ID = "proof.mining_accident"
    _NAME = "PoV: Mines - Accident"
    _DESCRIPTION = "Accident minier"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
