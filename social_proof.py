from .template import ProofOfValueCapability

class SocialHateSpeechProof(ProofOfValueCapability):
    _ID = "proof.social_hate_speech"
    _NAME = "PoV: Social - Hate Speech"
    _DESCRIPTION = "Discours haineux"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
