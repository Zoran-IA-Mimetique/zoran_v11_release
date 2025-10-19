# 🔒 Zoran🦋 Adapti — Audit Veritas Ready Proof Pack
**Version :** 1.0 – 2025-10-19  
**Auteur :** Frédéric Tabary — Institut IA Lab Inc.  
**Hash du PDF signé :** d3e136da3ca99bba1d11ffc537e7af5b85a2bc1ef865c3b4f8c4be25d152fefb493b32f6710a1224356594efe7f4038e4466dac116a706d7bd7a62399df942c5

---
## 1️⃣ Objet
Ce pack démontre la faisabilité d’un audit complet : SHA-512 + signature RSA + PQC + horodatage RFC 3161 + manifestes + logs.

## 2️⃣ Vérification rapide
```bash
sha512sum "ZORAN-ADAPTI (2).pdf"
openssl dgst -sha512 -verify zoran_demo_pub.pem \
  -signature "ZORAN-ADAPTI (2).pdf.sig" "ZORAN-ADAPTI (2).pdf"
openssl ts -verify -data "ZORAN-ADAPTI (2).pdf" \
  -in "ZORAN-ADAPTI (2).pdf.tsr" -CAfile "tsa_cert.pem"
```

## 3️⃣ Checklist conformité
| Domaine | Référence | Statut |
|----------|------------|--------|
| Intégrité | ISO 42001 §8.3 | ✅ |
| Authenticité | AI Act art 9–10 | ✅ |
| Horodatage | ETSI EN 319 421 | ✅ |
| Traçabilité | IEEE 7000 §6 | ✅ |
| Auditabilité | Veritas AI Audit | ✅ |
| Transparence publique | FAIR | 🔜 |

## 4️⃣ Roadmap
1. Signature eIDAS (qualifiée)
2. TSA Bureau Veritas
3. Publication GitHub / Zenodo
4. Vérification publique

*“La confiance se prouve, pas se proclame.”*
