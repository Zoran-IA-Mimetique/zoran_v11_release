# REBUILD FROM FLAT

Ce zip contient **2 dossiers plats** (`pkg-a`, `pkg-b`).  
Chaque fichier correspond à un chemin canonique mappé dans `MANIFEST.csv` (colonnes: `canonical_path,flat_filename,package_folder`).

## Reconstruction de l'arborescence

Exemple (bash) :
```bash
while IFS=',' read -r canonical flat pkg; do
  mkdir -p "$(dirname "$canonical")"
  cp "$pkg/$flat" "$canonical"
done < MANIFEST.csv
```
