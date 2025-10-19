#!/usr/bin/env bash
set -e
REPO="AIformpro/Zoran-2040-aSiM-Towards-a-Public-Ethical-and-Resilient-Super-Intelligence"
TAG="veritas-proof-$(date +%Y%m%d)"
MSG="Zoran🦋 Proof Pack – Audit Veritas Ready"
gh release create "$TAG" "zoran_evidence_pack.zip" --repo "$REPO" --notes "$MSG"
