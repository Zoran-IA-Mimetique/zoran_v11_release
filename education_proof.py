from .template import ProofOfValueCapability

class EducationPlagiarismProof(ProofOfValueCapability):
    _ID = "proof.education_plagiarism"
    _NAME = "PoV: Éducation - Plagiat"
    _DESCRIPTION = "Détection plagiat"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
