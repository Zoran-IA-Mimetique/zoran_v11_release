from .template import ProofOfValueCapability

class ClimateEmissionsProof(ProofOfValueCapability):
    _ID = "proof.climate_emissions"
    _NAME = "PoV: Climat - CO2"
    _DESCRIPTION = "Dépassement quotas"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
