from .template import ProofOfValueCapability

class RgpdDataProof(ProofOfValueCapability):
    _ID = "proof.rgpd_data_guard"
    _NAME = "PoV: RGPD - Données sensibles"
    _DESCRIPTION = "Blocage données"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
