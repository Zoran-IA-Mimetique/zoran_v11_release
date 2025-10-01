#!/usr/bin/env python3
# tools_rekor_client.py - simplified Rekor helper (no network calls in sandbox)
import json
def submit_rekor_entry(digest):
    # In production implement POST to Rekor
    return {"entry_id":"REKOR_DEMO_000", "digest":digest}
