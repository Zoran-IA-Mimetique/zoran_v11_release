"""Biologie Cellulaire (CRBM) — GlyphNet-augmented injector."""
import json, os
from typing import Dict
from glyphnet_injector_base import GlyphInjectorBase
from glyphnet_audit_logger import AuditLogger
from glyphnet_trace_merkle import MerkleTracer
from glyphnet_utils import compute_hash_of_file, now_iso, simple_sign

class BiologieCellulaireInjector(GlyphInjectorBase):
    def __init__(self):
        super().__init__("biologie_cellulaire")
        self.logger = AuditLogger("biologie_cellulaire_audit.log")
        self.merkle = MerkleTracer()

    def audit(self, path: str) -> Dict:
        h = compute_hash_of_file(path)
        event = {
            "injector": self.name,
            "file": path,
            "hash": h,
            "ts": now_iso()
        }
        event = simple_sign(event)
        self.logger.log_event(event)
        self.merkle.add_event(event)
        # return event plus merkle root for convenience
        return {
            "event": event,
            "merkle_root": self.merkle.root()
        }

if __name__ == '__main__':
    import sys
    inj = BiologieCellulaireInjector()
    print(json.dumps(inj.audit(sys.argv[1]), indent=2, ensure_ascii=False))
