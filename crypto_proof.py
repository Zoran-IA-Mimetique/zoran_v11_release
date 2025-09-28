from .template import ProofOfValueCapability

class CryptoTxProof(ProofOfValueCapability):
    _ID = "proof.crypto_tx"
    _NAME = "PoV: Crypto - Tx Suspecte"
    _DESCRIPTION = "Transaction suspecte"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
