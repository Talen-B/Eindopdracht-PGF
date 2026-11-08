from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt

console = Console()

def show_menu(title, options, body=None):
    items = "\n".join(
        f"[cyan]{number}[/cyan] - {label}"
        for number, label in enumerate(options, start=1)
    )

    # if body:
    #     content = f"{body}\n\n[bold]Actions[/bold]\n{items}"
    # else:
    #     content = items
    #
    content = f"{body}\n\n[bold]Actions[/bold]\n{items}" if body else items

    console.print(Panel(
        content,
        title=f"[bold yellow]{title}[/bold yellow]",
        border_style = "green",
        width = 48,
    ))

    try:
        choice = int(Prompt.ask("[bold cyan]Choice[/bold cyan]"))

        if 1 <= choice <= len(options):
            return choice

        console.print("[red]Please select a valid option![/red]")

    except ValueError:
        console.print("[red]Please enter a number![/red]")
