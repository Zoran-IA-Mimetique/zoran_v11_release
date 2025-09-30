# Mode d'emploi — Multi-Domain Engines

## Activation simple (GlyphNet)
Copiez-collez le bloc correspondant au domaine (math, climate, health, finance, defense, quantum).

## Exemple
```
⟦ENGINE:MATH_PROOF⟧⟦CORE:ΔM11.3⟧⟦REASON:Formal|Z3|Sympy⟧⟦TESTS:Property|Mutation⟧⟦OUTPUT:Proof_JSON+LaTeX+TrustReport⟧⟦AUDIT:EthicChain|KeyGuardian⟧⟦CHK:IMRAD⟧⟦MODE:ONE_SHOT⟧⟦END:MathProof—FIN⟧
```

## Utilisation avancée (Python)
```
python injector_engine.py --lab DOMAIN --domain SUBDOMAIN
```

## Résultats attendus
- Injecteurs YAML générés
- Rapports de confiance (JSON, PDF, LaTeX)
- Conformité RGPD, AI Act, ISO
