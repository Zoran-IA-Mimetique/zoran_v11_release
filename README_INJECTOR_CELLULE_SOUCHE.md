Injecteur « Cellule-Souche Polymorphe » — package release
===========================================================

Contenu (all files are at root of the zip package):
- injector_cellule_souche_polymorphe.yml
- injector_cellule_souche_polymorphe.b64
- decode_injector.sh
- README_INJECTOR_CELLULE_SOUCHE.md
- audit_log_merkle.json (placeholder)
- proofs_bundle.zip (placeholder)
- pr_checklist.md
- README_RUN_CI.md
- tools_kms_signer.py
- tools_rekor_client.py
- tools_krl_manager.py
- tools_verify_pipeline.py
- redteam_sim_quantum_forgery.py
- redteam_harness_local.py
- scripts_sign_and_anchor.sh
- scripts_migrate_sha512.sh
- .github_workflow_hsm_rekor_krl.yml
- .github_workflow_redteam_gate.yml

SHA-256 (injector YAML):
6ff07b3c10c488448f9ce4ba43d4d03272ae766e40d4a970cbbcd9dd0539753d

Notes:
- In sandbox (LLM) some external operations are stubbed: no HSM, no TSA, no Rekor network calls.
- In production (self-hosted runner) configure secrets, HSM/KMS, Rekor endpoint and TSA to produce verifiable proofs.

Usage:
1. Unpack or decode the injector YAML.
2. Review and adapt configuration (key ids, endpoints).
3. Run the pipeline on a self-hosted runner to produce audit_log_merkle.json and proofs_bundle.zip.
