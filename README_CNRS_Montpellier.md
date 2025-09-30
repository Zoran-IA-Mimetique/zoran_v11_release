# Zoran CNRS Montpellier Edition

Ce bundle contient tous les injecteurs YAML spécifiques pour les laboratoires CNRS de Montpellier :
- **CRBM** (biologie cellulaire, mécano-signalisation, cancer, imagerie, ICAP-1)
- **IGMM** (génomique, virologie, immunité, vaccins, bioinformatique, épigénétique)
- **IBMM** (chimie bio, peptides, métabolomique, matériaux, chimie verte)
- **LEM** (microbiologie, infection, métagénomique, environnement)
- **LIRMM** (robotique, IA, robotique médicale et industrielle, IA cognitive)
- **IES** (capteurs, électronique, photonique, hardware security)
- **LUPM** (astrophysique, physique quantique, astroparticules)

## Utilisation

1. Cloner le dépôt Zoran :
```bash
git clone https://github.com/Zoran-IA-Mimetique/zoran_v11_release
cd zoran_v11_release
```

2. Exécuter un injecteur avec `glyphnet` :
```bash
glyphnet run injectors/<nom_injecteur>.yaml --output ./outputs
```

3. Chaque injecteur produit un **Trust Report JSON** et un **log ZDM** auditable.

## Contenu

- 50+ injecteurs couvrant toutes les thématiques CNRS Montpellier.
- Gouvernance éthique (EthicChain, AI Act, ISO/IEC 42001).
- Fédérations multi-labos (PolyResonator consensus).
