# Zoran L2C Edition — Laboratoire Charles Coulomb (CNRS Montpellier)

Ce bundle contient tous les injecteurs YAML générés pour couvrir les thématiques de recherche du L2C :
- Verres structuraux et défauts
- Matière molle et colloïdes
- Nanostructures et spectroscopie (Raman, IR, XPS)
- Optique et photonique (non-linéaire, lasers, excitons)
- Matériaux 2D (graphène)
- Magnétoélectricité et spintronique
- Physique quantique théorique (Monte Carlo, QMC, dynamique moléculaire)
- Matériaux pour l’énergie (batteries, catalyse, stockage)
- Interfaces bio/physique
- HPC et calcul intensif (LAMMPS, Gromacs, simulations massives)

## Utilisation

1. Cloner le dépôt Zoran :
```bash
git clone https://github.com/Zoran-IA-Mimetique/zoran_v11_release
cd zoran_v11_release
```

2. Exécuter un injecteur avec glyphnet :
```bash
glyphnet run injectors/<nom_injecteur>.yaml --output ./outputs
```

Chaque injecteur produit un **Trust Report JSON** et un **log ZDM** auditable.
