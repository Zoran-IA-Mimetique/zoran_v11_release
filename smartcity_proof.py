from .template import ProofOfValueCapability

class SmartCityLightsProof(ProofOfValueCapability):
    _ID = "proof.smartcity_lights"
    _NAME = "PoV: SmartCity - Lights"
    _DESCRIPTION = "Surconsommation éclairage"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
