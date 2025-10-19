#!/usr/bin/env bash
curl -s -H "Authorization: Bearer $ZENODO_TOKEN" \
 -F "metadata={\"title\":\"Zoran🦋 Proof Pack\",\"upload_type\":\"dataset\"};type=application/json" \
 -F "file=@zoran_evidence_pack.zip" \
 https://zenodo.org/api/deposit/depositions
