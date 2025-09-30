import os, yaml, json

labs = json.load(open("labs_catalog.json", encoding="utf-8"))

AXES_TO_CAPS = {
    "adhésion cellulaire": ["core.loader", "glyphnet.instrumentation", "tests.property_based"],
    "YAP-TAZ": ["tests.mutation"],
    "intégrines β1": ["governance.trust_report"],
    "génomique": ["core.loader", "glyphnet.instrumentation", "compliance.rgpd_anonymizer"],
    "virologie": ["tests.property_based", "governance.trust_report"],
    "bioinformatique": ["engines.sandbox"],
    "peptides": ["core.loader", "glyphnet.instrumentation", "tests.mutation"],
    "protéomique": ["tests.property_based", "governance.trust_report"],
    "métabolomique": ["engines.sandbox"],
    "robotique": ["core.loader", "safety.policy", "tests.chaos"],
    "IA": ["glyphnet.instrumentation", "tests.property_based"],
    "cognition": ["engines.sandbox", "governance.trust_report"]
}

def build_injector(lab):
    caps = []
    for axe in lab["axes"]:
        caps += AXES_TO_CAPS.get(axe, [])
    seen, caps_unique = set(), []
    for c in caps:
        if c not in seen:
            caps_unique.append(c)
            seen.add(c)
    injector = {
        "id": f"injector_{lab['name'].lower()}",
        "title": f"Injecteur — {lab['name']} (auto-généré)",
        "version": "0.1.0",
        "metadata": {"purpose": f"Injecteur pour {lab['name']}"},
        "pipeline": [],
        "outputs": [{"name": "trust_report", "path": f"./outputs/{lab['name'].lower()}_trust.json"}]
    }
    for cap in caps_unique:
        entry = {"capability": cap, "params": {}}
        if cap == "core.loader":
            entry["params"] = {"path": f"workspace/{lab['name']}/", "entry_point": lab["entry_point"]}
        if cap == "tests.property_based":
            entry["params"] = {"module": f"tests/test_{lab['name'].lower()}.py"}
        if cap == "tests.mutation":
            entry["params"] = {"threshold": 80}
        if cap == "compliance.rgpd_anonymizer":
            entry["params"] = {"fields_to_anonymize": ["patient_id", "sample_id"]}
        if cap == "governance.trust_report":
            entry["params"] = {"sign_with": "KeyGuardian"}
        injector["pipeline"].append(entry)
    return injector

def main():
    os.makedirs("generated_injectors", exist_ok=True)
    for lab in labs:
        inj = build_injector(lab)
        out_path = f"generated_injectors/injector_{lab['name'].lower()}.yaml"
        with open(out_path, "w", encoding="utf-8") as f:
            yaml.dump(inj, f, sort_keys=False, allow_unicode=True)
        print("Injecteur généré :", out_path)

if __name__ == "__main__":
    main()
