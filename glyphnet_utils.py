"""GlyphNet utilities: hashing, time, simple PQC placeholder"""
import hashlib, json
from datetime import datetime

def compute_hash_of_file(path: str, algo: str = "sha512") -> str:
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"

def simple_sign(event: dict) -> dict:
    # placeholder deterministic 'signature' for reproducibility (not real crypto)
    s = json.dumps(event, sort_keys=True).encode("utf-8")
    event["glyph_signature"] = hashlib.sha256(s).hexdigest()
    return event
