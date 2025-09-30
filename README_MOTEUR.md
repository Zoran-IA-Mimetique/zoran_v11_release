# Moteur à Injecteurs Zoran v11 — Production

Ce moteur génère automatiquement des injecteurs YAML spécifiques pour les laboratoires CNRS.

## Contenu
- moteur_injecteurs.py : script Python de génération
- labs_catalog.json : catalogue des labos et axes de recherche
- injector_*.yaml : exemples générés (CRBM, IGMM, IBMM, LIRMM)

## Utilisation
```bash
python moteur_injecteurs.py
```
Résultat : les fichiers YAML apparaissent dans le dossier `generated_injectors/`.
