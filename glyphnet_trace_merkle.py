"""Simple Merkle tracer (toy implementation suitable for audit logs)."""
import hashlib, json
from typing import List, Dict

class MerkleTracer:
    def __init__(self):
        self.leaves = []

    def _leaf_hash(self, obj) -> str:
        s = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
        return hashlib.sha256(s).hexdigest()

    def add_event(self, event: Dict) -> str:
        h = self._leaf_hash(event)
        self.leaves.append(h)
        return h

    def root(self) -> str:
        # simple iterative pairwise hash
        nodes = self.leaves[:]
        if not nodes:
            return ""
        while len(nodes) > 1:
            next_nodes = []
            for i in range(0, len(nodes), 2):
                a = nodes[i]
                b = nodes[i+1] if i+1 < len(nodes) else nodes[i]
                combined = (a + b).encode("utf-8")
                next_nodes.append(hashlib.sha256(combined).hexdigest())
            nodes = next_nodes
        return nodes[0]
