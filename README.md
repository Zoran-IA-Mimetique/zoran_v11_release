# 🦋 Zoran / GlyphNet v11 — Towards a Public, Ethical & Resilient Super-Intelligence

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16940525.svg)](https://doi.org/10.5281/zenodo.16940525)
[![Reproducibility](https://img.shields.io/badge/Reproducibility-Open%20Science-blue)](https://zoran-2040-asim-swxr6lh.gamma.site/)
[![AI Act](https://img.shields.io/badge/EU%20AI%20Act-Ready-orange)](https://artificialintelligenceact.eu/)
[![ISO/IEC 42001](https://img.shields.io/badge/ISO/IEC-42001-informational)](https://www.iso.org/standard/81230.html)

---

## 🔎 Introduction

**Zoran / GlyphNet v11** est le premier **framework open-source** conçu comme un **système d’exploitation pour l’IA de confiance**.  
Il combine **code exécutif**, **Charte Constitutionnelle**, **mécanismes de gouvernance éthique**, et **preuves académiques**.

👉 Objectif : fournir une **infrastructure publique, éthique et résiliente** pour l’IA, en conformité avec le **RGPD**, l’**AI Act**, et **ISO/IEC 42001**.

---

## 📂 Contenu

Ce dépôt regroupe :

- **Code opérationnel**  
  - Plugins : mathématiques, sciences sociales, NLP, neuro, sécurité, gouvernance, core.  
  - Federation persistante (SQLite).  
  - ZDM avec persistance disque.  
  - Sandbox renforcé.  
  - CLI complète + guides plugins.

- **Sécurité & Gouvernance**  
  - KeyGuardian (TPM, advisory lock, threshold signing, containment, CognitiveGuardian).  
  - EthicChain + ZDM (Merkle + PQC).  
  - Revocation Policy, Integrity Policy, Public Keys fingerprints.  
  - GEPs (000 → 005) : cadence, sunset clause, rollout, metrics, gouvernance, opt-out.

- **Tests avancés**  
  - Chaos, mutation, property-based, performance.

- **POC sectoriels**  
  - Santé, finance, énergie, justice, BTP, mobilité, défense, climat, éducation.  
  - Pack injecteurs YAML (France Travail, CNIL, ONU, OTAN, CNRS, EDF, etc.).  
  - POC ultra-frugal (1 téléphone / 1 personne / 9 mois).

- **Documentation académique**  
  - White Papers (IMRaD, Low Carbon, Civilisationnel, Omega).  
  - Roadmaps TRL8 → TRL12.  
  - Communication Strategy.  
  - Limitations connues (fatigue sociale, oracles, incitations).  
  - Glossaire, index global, backlog.  

- **Philosophie**  
  - La Quête du Loup (thèses + réfutations).  
  - Architecte Humble.  
  - Constitution Zoran Ω.  
  - Vision civilisationnelle.
  - 

---## 📦 Injecteurs CNRS Montpellier — Extensions Zoran v11

Ce module complète le projet avec une série d’injecteurs spécialisés couvrant les laboratoires CNRS de Montpellier.  
Chaque injecteur existe en deux variantes :  

- **Python pur** : vérification simple, audit de base  
- **Python augmenté GlyphNet** : instrumentation avancée (Merkle, journalisation auditable, signatures glyphiques, conformité AI Act / RGPD / ISO 42001)  

### 🔬 Domaines couverts
- **Biologie cellulaire (CRBM)** → `injecteur_biologie_cellulaire.py` / `_glyph.py`  
- **Génétique moléculaire (IGMM)** → `injecteur_genetique.py` / `_glyph.py`  
- **Infectiologie (IRIM)** → `injecteur_infectiologie.py` / `_glyph.py`  
- **Mathématiques / optimisation (IMAG)** → `injecteur_math_model.py` / `_glyph.py`  
- **Géosciences Montpellier** → `injecteur_geosciences.py` / `_glyph.py`  
- **Écologie & vecteurs (MIVEGEC)** → `injecteur_ecologie.py` / `_glyph.py`  
- **Chimie & matériaux (ENSCM, IEM, ICMM, IBMM)** → `injecteur_chimie.py` / `_glyph.py`  

### ⚙️ Exemple d’usage
```bash
# Audit simple
python injecteur_biologie_cellulaire.py fichier.fq

# Audit augmenté GlyphNet
python injecteur_biologie_cellulaire_glyph.py fichier.fq


## 📖 Structure

- `plugins_*` → Capacités métiers.  
- `federation_*` → API fédération persistante (SQLite).  
- `memory_zdm.py` → ZDM persistant.  
- `engines_sandbox.py` → Sandbox renforcé.  
- `cli_*` → CLI minimaliste et complète.  
- `tests_*` → Tests avancés (chaos, mutation, property, performance).  
- `injectors/*.yaml` → POC institutionnels (10 injecteurs stratégiques).  
- `docs/` → Documentation publique (politiques, roadmap, gouvernance, fatigue sociale).  
- `geps/` → GlyphNet Enhancement Proposals (000 → 005).  
- `whitepapers/*.md|.pdf` → Livres blancs académiques.  
- `scripts/` → Déploiement POC frugal, rollback, canary.  

---

## 📊 Roadmap

- **TRL8** → atteint (preuves PQC, ZKP, ZDM, SBOM, VEX).  
- **TRL9** → pilote réel (santé, énergie).  
- **TRL10–12** → adoption massive, internationale, planétaire.

Voir :  
- `docs/ROADMAP_TRL9.md`  
- `docs/ROADMAP_BEYOND_TRL9.md`  

---

## 📚 Publications associées

DOIs Zenodo :  
- [10.5281/zenodo.16940525](https://doi.org/10.5281/zenodo.16940525)  
- [10.5281/zenodo.16941007](https://doi.org/10.5281/zenodo.16941007)  
- [10.5281/zenodo.16940299](https://doi.org/10.5281/zenodo.16940299)  
- [10.5281/zenodo.16995014](https://doi.org/10.5281/zenodo.16995014)  
- [10.5281/zenodo.16995226](https://doi.org/10.5281/zenodo.16995226)  
- [10.5281/zenodo.16997156](https://doi.org/10.5281/zenodo.16997156)  

---

## 📜 Citation

Merci de citer ce travail comme :  

**Tabary, F. (2025). _Zoran / GlyphNet v11 — Towards a Public, Ethical & Resilient Super-Intelligence._ Institut IA Inc., Montréal / Angers. DOI:10.5281/zenodo.16940525**  

BibTeX :  

```bibtex
@misc{tabary2025zoran,
  author       = {Frédéric Tabary},
  title        = {Zoran / GlyphNet v11 — Towards a Public, Ethical & Resilient Super-Intelligence},
  year         = {2025},
  publisher    = {Institut IA Inc. Montréal / Angers},
  doi          = {10.5281/zenodo.16940525}
}


---

🧑‍💻 Auteur

👤 Frédéric Tabary
📍 Angers / Montréal
📧 tabary01@gmail.com
🏛️ Institut IA Inc.


---

© 2025 Frédéric Tabary — Licence MIT

---

👉 Ce README provisoire est **déjà publiable tel quel** : il contient badges, DOIs, structure, citation, et reflète l’intégralité de ce qu’on a produit.  

Veux-tu que je prépare aussi une **version courte (≤350 caractères)** qui pourra servir sur Zenodo/GitHub description ?
