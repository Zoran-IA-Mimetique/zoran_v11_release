from .template import ProofOfValueCapability

class EnergyOverloadProof(ProofOfValueCapability):
    _ID = "proof.energy_overload"
    _NAME = "PoV: Énergie - Surcharge"
    _DESCRIPTION = "Surconsommation électrique"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
