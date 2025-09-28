import typer
from . import audit, injector, plugin, init # Ajout de init

app = typer.Typer(
    name="glyphnet",
    help="Le système d'exploitation pour l'IA de Confiance - Outil en ligne de commande.",
    no_args_is_help=True
)

# Enregistrer les sous-commandes
app.add_typer(init.app, name="init") # Ajout de la nouvelle commande
app.add_typer(audit.app, name="audit")
app.add_typer(injector.app, name="injector")
app.add_typer(plugin.app, name="plugin")

if __name__ == "__main__":
    app()
