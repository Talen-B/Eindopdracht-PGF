from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def show_menu(title, options):
    items = "\n".join(
        f"[cyan]{number}[/cyan] - {label}"
        for number, label in enumerate(options, start=1)
    )

    console.print(Panel(
        f"{items}",
        title=f"[bold yellow]{title}[/bold yellow]",
        border_style = "green",
        width = 48,
    ))

    return Prompt.ask("[bold cyan]Choice[/bold cyan]")