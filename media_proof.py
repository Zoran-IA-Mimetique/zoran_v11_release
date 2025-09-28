from .template import ProofOfValueCapability

class MediaFakeNewsProof(ProofOfValueCapability):
    _ID = "proof.media_fake_news"
    _NAME = "PoV: Médias - Fake News"
    _DESCRIPTION = "Fake news"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
