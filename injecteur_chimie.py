"""Chimie / Matériaux — pure Python injector (non-instrumented)."""
import json
from datetime import datetime
from typing import Dict

def audit_chimie(path: str) -> Dict:
    """Perform a lightweight audit/check on the given file/path."""
    from glyphnet_utils import compute_hash_of_file, now_iso

    h = compute_hash_of_file(path)
    return {
        "injector": "chimie",
        "file": path,
        "hash": h,
        "ts": now_iso(),
        "status": "ok"
    }

if __name__ == '__main__':
    import sys
    print(json.dumps(audit_chimie(sys.argv[1]), indent=2, ensure_ascii=False))
