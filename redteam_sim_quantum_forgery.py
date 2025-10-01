#!/usr/bin/env python3
# redteam_sim_quantum_forgery.py - simulate hybrid signing & forgery
import os, json
from tools_kms_signer import create_signer
def run():
    cfg = {"type":"hybrid","classical":{"type":"local","private_key_hex": "a"*64},"pqc":{"type":"pqc_dilithium"}}
    # In sandbox, hybrid is simulated by creating dict
    sig = {"hybrid":True, "classical": {"key_id":"local_fallback"}, "pqc":{"key_id":"pqc_stub"}}
    print('SIMULATED HYBRID SIGNATURE:', json.dumps(sig))
if __name__=='__main__':
    run()
