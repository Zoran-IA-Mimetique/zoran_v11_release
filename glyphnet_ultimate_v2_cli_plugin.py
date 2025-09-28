import typer
from rich.console import Console
from rich.table import Table
from glyphnet_ultimate_v2.engines.capabilities import capability_registry

app = typer.Typer(name="plugin", help="Gère les plugins de capacités.")
console = Console()

@app.command(name="list", help="Liste tous les plugins de capacités disponibles.")
def list_plugins():
    """Affiche la liste des plugins découverts par le CapabilityRegistry."""
    console.print("🔎 [bold cyan]Liste des plugins de capacités disponibles...[/bold cyan]")
    
    plugins = capability_registry._capabilities
    
    if not plugins:
        console.print("[yellow]Aucun plugin trouvé. Assurez-vous que le package `glyphnet_ultimate_v2.plugins` est accessible.[/yellow]")
        return

    table = Table(title="Plugins Enregistrés")
    table.add_column("ID de la Capacité", style="green", no_wrap=True)
    table.add_column("Version", style="magenta")
    table.add_column("Description", style="white")

    for cap_id, cap_class in sorted(plugins.items()):
        instance = cap_class()
        meta = instance.metadata()
        table.add_row(
            meta.get("id", "N/A"),
            meta.get("version", "N/A"),
            meta.get("description", "")
        )
        
    console.print(table)
