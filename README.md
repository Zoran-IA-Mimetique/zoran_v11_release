# GlyphNet Ultimate — Zoran v11 (README Principal)

[![Build](https://img.shields.io/github/actions/workflow/status/zoran-labs/glyphnet/ci.yml?label=CI)](#)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](#)
[![Coverage](https://img.shields.io/badge/coverage-report-blue)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#)
[![PyPI](https://img.shields.io/pypi/v/glyphnet-ultimate.svg?label=PyPI)](#)

> **Ce README est le _README principal_ de l’ensemble.**  
> Il remplace et unifie les anciens README.  
> _Temps de prise en main (demande client) : ~1h30._

---

## Table des matières

- [Vision & Pitch](#vision--pitch)
- [Architecture & Périmètre](#architecture--périmètre)
- [Fonctionnalités Implémentées](#fonctionnalités-implémentées)
- [Installation](#installation)
- [Démos & Exemples](#démos--exemples)
- [Qualité & Sécurité](#qualité--sécurité)
- [Conformité EU (ETSI, AI Act)](#conformité-eu-etsi-ai-act)
- [Roadmap](#roadmap)
- [Licence](#licence)

---

## Vision & Pitch

GlyphNet est un **système d’exploitation pour l’IA de confiance** : gouvernance _as code_, traçabilité, cryptographie PQC et outils d’audit.  
Les documents fournis définissent la vision, les modules et les tests de référence.

## Architecture & Périmètre

- **Core** : modèle Pydantic immuable, signature/verif. PQC, moteurs fédérés.  
- **Gouvernance EU** : vérifications ETSI + prêt AI Act.  
- **IA avancée** : raisonnement neuro‑symbolique, RL éthique.  
- **ZKP** : génération/vérif. de preuves (simulation de référence).  
- **Fédération** : agrégation & consensus distribués.  
- **Outillage** : injecteurs YAML, sandbox plugins, CI/CD.

## Fonctionnalités Implémentées

- Modèle central, PQC (référence), conformité ETSI, ZKP (réf.), neuro‑symbolique, RL éthique, fédération.  
- **CI/CD** : lint, tests, coverage, publication PyPI (workflows fournis).  
- **Sécurité** : logs immuables, ZDM Merkle, SBOM & VEX (squelettes).

## Installation

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # (si présent)
# Sinon :
pip install pydantic pytest
```

## Démos & Exemples

Voir `glyphnet_ultimate/examples` et `glyphnet_ultimate/demonstration.py`.

## Qualité & Sécurité

- Tests unitaires (voir `glyphnet_ultimate/tests`).
- Journalisation immuable (`security/logger.py`) & mémoire ZDM (`memory/zdm.py`).
- Workflows GitHub Actions : `ci.yml`, `advanced_tests.yml`.

## Conformité EU (ETSI, AI Act)

- Vérifications programmatiques via `eu_standard/etsi.py`.
- Preuves partageables via `zkp/` (simulation) et signature PQC.

## Roadmap

Voir `ROADMAP.md` (standardisation, intégrations réelles liboqs/ZKP, MLOps).

## Licence

MIT — voir `LICENSE`.
