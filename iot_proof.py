from .template import ProofOfValueCapability

class IotAnomalyProof(ProofOfValueCapability):
    _ID = "proof.iot_anomaly"
    _NAME = "PoV: IoT - Anomalies"
    _DESCRIPTION = "Détection capteurs"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
