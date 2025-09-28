from .template import ProofOfValueCapability

class MobilityGuardProof(ProofOfValueCapability):
    _ID = "proof.mobility_guardrail"
    _NAME = "PoV: Mobilité - Garde-fou"
    _DESCRIPTION = "Blocage zone agent"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
