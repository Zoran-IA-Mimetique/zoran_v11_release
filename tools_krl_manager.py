#!/usr/bin/env python3
# tools_krl_manager.py - simplified KRL manager
import json, hashlib, base64
def create_signed_krl(revoked_keys, signer):
    krl = {"revoked_keys":revoked_keys}
    krl_json = json.dumps(krl, sort_keys=True, separators=(',',':')).encode()
    krl_hash = hashlib.sha512(krl_json).hexdigest()
    sig = signer.sign(krl_json)
    return {"krl":krl, "hash":krl_hash, "signature":sig}
