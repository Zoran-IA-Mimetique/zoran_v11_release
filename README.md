# ZORAN • GlyphNet — README Principal

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Build](https://img.shields.io/badge/build-GitHub_Actions-brightgreen.svg)](#) [![Coverage](https://img.shields.io/badge/coverage-codecov-blue.svg)](#) [![DOI](https://img.shields.io/badge/DOI-Zenodo_pending-lightgrey.svg)](#)

> **Ce README est le point d’entrée principal de *l’ensemble* des livrables Zoran/GlyphNet.**  
> Dernière génération : **2025-09-28 13:29 UTC**

## Résumé (court)
ZORAN/GlyphNet est une infrastructure de confiance pour l’IA : capacités stateless orchestrées en pipelines, mémoire ZDM, fédération distribuée, artefacts vérifiables (SBOM/C2PA), CI/CD et conformité (AI Act).

## Résumé (étendu)
Le projet consolide un noyau orienté *capabilities* (plugins) et un orchestrateur de pipelines. Il fournit des briques prêtes à l’emploi pour la simulation, la gouvernance, la sécurité et la conformité : ZDM persistante, PQC (liboqs), ZKP (ZoKrates), intégrations MLOps (MLflow), bus de messages (NATS), CI/CD, benchmarks et tests avancés (chaos, mutation). L’objectif est un dépôt GitHub **propre**, **reproductible** et **citables** par la communauté.

## Table des matières
- [Installation](#installation)
- [Structure du dépôt](#structure-du-dépôt)
- [Documentation (`docs/`)](#documentation-docs)
- [Batches de code (`batch_xxx/`)](#batches-de-code-batch_xxx)
- [QA & Vérifications](#qa--vérifications)
- [Citations & DOI](#citations--doi)

## Installation
Ce paquet est un *release bundle* à plat. L’installation via `pip install -e .` est optionnelle et concerne surtout les métadonnées.

```bash
pip install -e .  # optionnel
```

## Structure du dépôt
```
zoran_v11_release_batches/
├── README.md
├── CITATION.cff
├── LICENSE
├── pyproject.toml
├── docs/
│   ├── ZORAN_COMPLET_V11_AVEC_PITCH.md
│   ├── ZORAN_COMPLET_PYTHON_GLYPHNET_V11_SUITE_2.md
│   ├── ZORAN_COMPLET_GLYPHNET_PYTHON_3.md
│   ├── RAPPORT_EXECUTION_ETAPE_2.md
│   ├── RAPPORT_EXECUTION_ETAPE_3.md
│   ├── RAPPORT_EXECUTION_ETAPE_4.md
│   ├── RAPPORT_EXECUTION_ETAPE_5.md
│   └── EPILOGUE.md
├── batch_001/
│   ├── ... (≤ 100 fichiers)
└── batch_00N/
    └── ... (si nécessaire)
```

## Documentation (`docs/`)
- Étapes 2 → 5 & Épilogue : rapports détaillés, objectifs & résultats.
- Textes intégraux des sources pour traçabilité scientifique.

## Batches de code (`batch_xxx/`)
- **À plat** (flat), max **100 fichiers par dossier**.
- Nommage basé sur le chemin originel (séparateurs `/` remplacés par `_`).

## QA & Vérifications
- Vérification syntaxe Python (**10 passes** par fichier).
- Batching automatique ≤ 100 fichiers par dossier.
- Rapport QA dans `docs/QA_REPORT.md`.

## Citations & DOI
- Voir `CITATION.cff` (GitHub *Cite this repository*).
- DOI Zenodo : badge “pending” jusqu’à enregistrement du dépôt.
