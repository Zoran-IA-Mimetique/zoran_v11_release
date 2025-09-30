# Capability Federation Protocol
Permettre à plusieurs instances de Zoran de partager des capacités de manière sécurisée.

## Mode Serveur
- Expose certaines capabilities via API sécurisée (auth PQC).
- Fournit endpoint avec métadonnées + contrat de gouvernance.

## Mode Client
- Utilise core.remote_executor pour appeler une capability distante.
- Résultats intégrés comme si locaux.

## Impact
- Création d’un marché distribué de capacités cognitives.
- Mutualisation et monétisation sans exposer le code source.
