from .template import ProofOfValueCapability

class ElectionsAnomalyProof(ProofOfValueCapability):
    _ID = "proof.elections_anomaly"
    _NAME = "PoV: Élections - Anomalies"
    _DESCRIPTION = "Votes incohérents"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
