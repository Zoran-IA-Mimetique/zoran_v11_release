# 🦋 Zoran aSiM — Injector-Engine for Major Research Institutes
**Towards reproducible, auditable and compliant science across INSERM, CEA, INRIA, INRAE, IRD**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Release](https://img.shields.io/github/v/release/Zoran-IA-Mimetique/zoran_v11_release)](#)
[![Build Status](https://img.shields.io/github/actions/workflow/status/Zoran-IA-Mimetique/zoran_v11_release/ci.yml?branch=main)](#)
[![Tests](https://img.shields.io/github/actions/workflow/status/Zoran-IA-Mimetique/zoran_v11_release/advanced_tests.yml?branch=main&label=tests)](#)
[![Coverage](https://img.shields.io/codecov/c/github/Zoran-IA-Mimetique/zoran_v11_release)](#)
[![AI Act Ready](https://img.shields.io/badge/AI%20Act-Ready-blue)](#)
[![ISO/IEC 42001](https://img.shields.io/badge/ISO%2FIEC-42001-blueviolet)](#)
[![EthicChain](https://img.shields.io/badge/EthicChain-Active-brightgreen)](#)
[![KeyGuardian](https://img.shields.io/badge/KeyGuardian-PQC-orange)](#)
[![Open Science](https://img.shields.io/badge/Open%20Science-✓-green)](#)

---

## 📖 Introduction
This repository hosts the **Injector-Engine**, a polymorphic generator capable of producing specialized injectors for France’s major research institutes: INSERM, CEA, INRIA, INRAE, IRD.

The engine guarantees:
- **Reproducibility**: IMRaD-structured outputs, Trust Reports.
- **Auditability**: mutation/property/chaos testing.
- **Compliance**: GDPR, AI Act, ISO/IEC 42001.

---

## ⚡ Quickstart

### GlyphNet one-shot block
```
⟦INJECTOR:ENGINE:POLYMORPH⟧⟦CORE:ΔM11.3⟧⟦MODE:ONE_SHOT⟧⟦TARGET:INSERM,CEA,INRIA,INRAE,IRD⟧⟦AUTO:Selector⟧⟦OUTPUT:yaml,python,trust_json,pdf⟧⟦AUDIT:EthicChain|ZDM|KeyGuardian⟧⟦TESTS:mutation|property|chaos⟧⟦CHK:IMRAD|VALIDATION|RGPD|AI_ACT|ISO42001⟧⟦LEN:EXHAUSTIVE⟧⟦END:InjectorEngine_allLabs—FIN⟧
```

### Docker
```bash
git clone https://github.com/Zoran-IA-Mimetique/injector_engine_alllabs.git
cd injector_engine_alllabs
docker-compose up
```

### Python
```bash
git clone https://github.com/Zoran-IA-Mimetique/injector_engine_alllabs.git
cd injector_engine_alllabs
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python injector_engine.py --lab INSERM --domain imaging
```

---

## 📦 Contents
- `injector_engine.glyph` — GlyphNet compressed engine block
- `injector_engine.yaml` — YAML engine configuration & mappings
- `injector_insrem_imaging.yaml` — example INSERM injector
- `injector_inria_ml.yaml` — example INRIA injector
- `injector_cea_hpc.yaml` — example CEA injector
- `injector_inrae_agro.yaml` — example INRAE injector
- `injector_ird_epi.yaml` — example IRD injector
- `mode_emploi.md` — usage guide
- `whitepaper_injector_engine.md` — IMRaD white paper
- `trust_report_template.json` — trust report template
- `plugins/` — plugin skeletons
- `tests/` — mutation/property/chaos tests
- `docker-compose.yml` — docker orchestrator
- `CHANGELOG.md`, `LICENSE.md`

---

© 2025 Frédéric Tabary — Institut IA Inc. — MIT License
