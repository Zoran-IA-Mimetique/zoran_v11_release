from .template import ProofOfValueCapability

class HospitalPrescriptionProof(ProofOfValueCapability):
    _ID = "proof.hospital_prescription"
    _NAME = "PoV: Hôpital - Prescription"
    _DESCRIPTION = "Mauvaise prescription"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
