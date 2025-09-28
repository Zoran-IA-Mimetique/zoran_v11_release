import typer
import yaml
from rich.console import Console
import json

from glyphnet_ultimate_v2.injectors.composer import PipelineComposer

app = typer.Typer(name="injector", help="Exécute des pipelines d'injection.")
console = Console()

@app.command(name="run", help="Exécute un pipeline défini dans un fichier YAML.")
def run_injector(
    config_path: str = typer.Argument(..., help="Chemin vers le fichier de configuration du pipeline YAML."),
    initial_context_json: str = typer.Option("{}", "--context", "-c", help="Contexte initial au format JSON.")
):
    """Exécute un pipeline d'injection et affiche le contexte final."""
    console.print(f"🚀 [bold green]Exécution du pipeline :[/bold green] {config_path}")

    try:
        initial_context = json.loads(initial_context_json)
    except json.JSONDecodeError:
        console.print(f"❌ [bold red]Erreur : Le contexte fourni n'est pas un JSON valide.[/bold red]")
        raise typer.Exit(code=1)

    try:
        composer = PipelineComposer(config_path)
        final_context = composer.execute(initial_context)
        
        console.print("\n--- [bold]Contexte Final[/bold] ---")
        console.print_json(data=final_context)
        
    except FileNotFoundError:
        console.print(f"❌ [bold red]Erreur : Fichier de configuration non trouvé à '{config_path}'.[/bold red]")
        raise typer.Exit(code=1)
    except (ValueError, RuntimeError, TypeError) as e:
        console.print(f"❌ [bold red]Erreur lors de l'exécution du pipeline : {e}[/bold red]")
        raise typer.Exit(code=1)
# tests/test_chaos_federation.py
import pytest
import httpx
import random
import time
from fastapi.testclient import TestClient
from glyphnet_ultimate_v2.federation.api import app, database

# Configurer une base de données de test en mémoire pour l'isolation
@pytest.fixture(autouse=True)
def test_db():
    database.DB_PATH = ":memory:"
    database.init_db()
    yield
    # Pas besoin de nettoyer, la DB en mémoire est détruite

client = TestClient(app)

# Monkey-patch httpx pour simuler des pannes réseau
_original_post = httpx.post

def chaotic_post(*args, **kwargs):
    """Wrapper qui injecte des pannes (timeout, erreur 500) aléatoirement."""
    roll = random.random()
    if roll < 0.2: # 20% de chance de timeout
        raise httpx.TimeoutException("Request timed out due to chaos engineering.")
    if 0.2 <= roll < 0.3: # 10% de chance d'erreur serveur
        return httpx.Response(500, json={"detail": "Internal Server Error due to chaos."})
    return _original_post(*args, **kwargs)

@pytest.mark.chaos
def test_federation_resilience_under_chaos(monkeypatch):
    """
    Teste que le système de vote reste cohérent malgré des pannes réseau simulées.
    """
    # Remplacer la fonction `post` par notre version chaotique pour les clients simulés
    monkeypatch.setattr(httpx, "post", chaotic_post)

    # 1. Soumettre une proposition via le client de test fiable
    response = client.post("/proposals", json={"proposer_id": "chaos_master", "claim": "Test resilience", "details": {}})
    assert response.status_code == 201
    proposal_id = response.json()["proposal_id"]

    # 2. Simuler 50 agents qui tentent de voter, certains vont échouer
    successful_votes = 0
    total_attempts = 50
    for i in range(total_attempts):
        try:
            # On utilise le client httpx patché pour simuler les votes des agents
            # Le TestClient de FastAPI ne passe pas par la couche réseau réelle, donc il n'est pas patché.
            # On simule un appel externe.
            res = httpx.post(f"http://testserver/votes", json={"voter_id": f"agent_{i}", "proposal_id": proposal_id, "decision": True})
            if res.status_code == 200:
                successful_votes += 1
        except httpx.TimeoutException:
            pass # On s'attend à ces échecs

    # 3. Vérifier l'état final du système via le client de test fiable
    response = client.get(f"/results/{proposal_id}")
    assert response.status_code == 200
    results = response.json()

    # Assertion Clé : L'état de la base de données doit être cohérent.
    # Le nombre de votes enregistrés doit correspondre exactement au nombre de requêtes POST qui ont réussi.
    assert results["total_votes"] == successful_votes
    assert results["votes_for"] == successful_votes
    assert results["votes_against"] == 0
