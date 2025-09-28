import os
import typer
from rich.console import Console

app = typer.Typer(name="init", help="Initialise un nouveau projet GlyphNet.")
console = Console()

TEMPLATE_DIRS = [
    "config/injectors",
    "plugins/custom",
    "tests",
    "scripts"
]

TEMPLATE_FILES = {
    ".glyphnet_project": "# Fichier marqueur pour les projets GlyphNet",
    "config/injectors/default_pipeline.yaml": """
name: "Default Example Pipeline"
description: "Un pipeline de démarrage pour votre projet."
pipeline:
  - capability: "core.stateless_logger"
    params:
      action: "log"
      current_state:
        logs: []
      message: "Pipeline started"
    output_as: "log_result"
""",
    ".gitignore": """
# Python
__pycache__/
*.pyc
venv/

# GlyphNet
*.db
glyphnet_storage/
"""
}

@app.command(name="project", help="Crée la structure de base d'un projet GlyphNet dans le répertoire courant.")
def init_project():
    """Crée l'arborescence et les fichiers de configuration de base."""
    console.print("🚀 [bold green]Initialisation d'un nouveau projet GlyphNet...[/bold green]")
    
    try:
        for directory in TEMPLATE_DIRS:
            os.makedirs(directory, exist_ok=True)
            console.print(f"   [dim]Créé :[/dim] {directory}/")
            
        for file_path, content in TEMPLATE_FILES.items():
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    f.write(content.strip())
                console.print(f"   [dim]Créé :[/dim] {file_path}")
        
        console.print("\n✅ [bold green]Projet initialisé avec succès ![/bold green]")
        console.print("Prochaines étapes :")
        console.print("1. Créez vos plugins dans le répertoire `plugins/`.")
        console.print("2. Définissez vos pipelines dans `config/injectors/`.")
        console.print("3. Exécutez vos pipelines avec `glyphnet injector run config/injectors/your_pipeline.yaml`.")
    except OSError as e:
        console.print(f"❌ [bold red]Erreur lors de la création du projet : {e}[/bold red]")
        raise typer.Exit(code=1)
