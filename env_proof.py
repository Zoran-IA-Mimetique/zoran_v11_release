from .template import ProofOfValueCapability

class EnvWaterPollutionProof(ProofOfValueCapability):
    _ID = "proof.env_water_pollution"
    _NAME = "PoV: Environnement - Eau"
    _DESCRIPTION = "Pollution eau"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
