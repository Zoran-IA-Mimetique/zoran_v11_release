# vnmi.py — Exemple simple d’utilisation de l’injecteur VNMI

def main(data: str):
    print(f"[VNMI] Traitement des données : {data}")
    return {"status": "ok", "processed_data": data}

if __name__ == "__main__":
    example_data = "demo_VNMI_data"
    result = main(example_data)
    print("Résultat VNMI :", result)
