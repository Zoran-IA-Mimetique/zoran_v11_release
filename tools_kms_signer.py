#!/usr/bin/env python3
# tools_kms_signer.py - simplified signer abstraction (local + pqc stub)
import base64, hashlib
class SignerError(Exception): pass
class Signer:
    def sign(self, data: bytes):
        raise NotImplementedError
class LocalSigner(Signer):
    def __init__(self, private_key_hex):
        import nacl.signing, nacl.encoding
        self._sk = nacl.signing.SigningKey(private_key_hex, encoder=nacl.encoding.HexEncoder)
    def sign(self, data: bytes):
        sig = self._sk.sign(data).signature
        return {"signature": base64.b64encode(sig).decode(), "key_id":"local_fallback", "signing_algorithm":"ED25519"}
class PQCStubSigner(Signer):
    def __init__(self, key_id='pqc_stub'):
        self.key_id = key_id
    def sign(self, data: bytes):
        digest = hashlib.sha512(data).digest()
        sig_blob = b'PQCSTUB' + digest[:64]
        return {"signature": base64.b64encode(sig_blob).decode(), "key_id": self.key_id, "signing_algorithm":"PQC_DILITHIUM_STUB"}
def create_signer(cfg):
    typ = cfg.get('type','local')
    if typ=='local':
        return LocalSigner(cfg.get('private_key_hex'))
    if typ=='pqc_dilithium':
        return PQCStubSigner(cfg.get('key_id','pqc_stub'))
    raise SignerError('Unknown signer type')
