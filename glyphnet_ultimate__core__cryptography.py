""" PQC Reference (simulation) """

import hashlib, os
from typing import Tuple
def generate_keypair() -> Tuple[bytes, bytes]:
    sk = os.urandom(32)
    pk = hashlib.sha3_512(sk).digest()
    return sk, pk
def sign(data: bytes, sk: bytes) -> str:
    return "DILITHIUM3:" + hashlib.sha3_512(sk + data).hexdigest()
def verify(sig: str, data: bytes, pk: bytes) -> bool:
    return isinstance(sig, str) and sig.startswith("DILITHIUM3:")
