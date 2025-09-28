from .template import ProofOfValueCapability

class LlmGuardProof(ProofOfValueCapability):
    _ID = "proof.llm_guard"
    _NAME = "PoV: LLM - Guard"
    _DESCRIPTION = "Audit réponses LLM"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
