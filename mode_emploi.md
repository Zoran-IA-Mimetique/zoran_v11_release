# Mode d'emploi — Injector-Engine AllLabs

## Activation simple
Copiez-collez le bloc GlyphNet :
```
⟦INJECTOR:ENGINE:POLYMORPH⟧⟦CORE:ΔM11.3⟧⟦MODE:ONE_SHOT⟧⟦TARGET:INSERM,CEA,INRIA,INRAE,IRD⟧⟦AUTO:Selector⟧⟦OUTPUT:yaml,python,trust_json,pdf⟧⟦AUDIT:EthicChain|ZDM|KeyGuardian⟧⟦TESTS:mutation|property|chaos⟧⟦CHK:IMRAD|VALIDATION|RGPD|AI_ACT|ISO42001⟧⟦LEN:EXHAUSTIVE⟧⟦END:InjectorEngine_allLabs—FIN⟧
```

## Générer un injecteur spécifique
```bash
python injector_engine.py --lab INSERM --domain imaging
```

## Trust Reports
Les injecteurs produits émettent automatiquement des rapports de confiance (JSON, PDF, LaTeX) signés par KeyGuardian.
