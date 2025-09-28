from .template import ProofOfValueCapability

class CyberBruteforceProof(ProofOfValueCapability):
    _ID = "proof.cybersecurity_bruteforce"
    _NAME = "PoV: Cyber - Bruteforce"
    _DESCRIPTION = "Détection brute force"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
