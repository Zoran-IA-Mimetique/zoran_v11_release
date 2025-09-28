from .template import ProofOfValueCapability

class SupplyChainProof(ProofOfValueCapability):
    _ID = "proof.supply_chain_stock"
    _NAME = "PoV: Supply - Stocks"
    _DESCRIPTION = "Rupture stocks"

    def _run_proof_logic(self):
        return True, "Demo passed", {}
