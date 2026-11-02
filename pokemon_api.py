import requests
from rich.console import Console
from rich.panel import Panel

console = Console()
BASE_URL = "https://pokeapi.co/api/v2"
TIMEOUT = 10

def get_pokemon(name):
    response = requests.get(
        f"{BASE_URL}/pokemon/{name}/",
        timeout=TIMEOUT
    )
    response.raise_for_status()

    return response.json()

def show_pokemon(pokemon):
    types = ", ".join(
        item["type"]["name"].capitalize()
        for item in pokemon["types"]
    )

    abilities = ", ".join(
        item["ability"]["name"].replace("-", " ").title()
        for item in pokemon["abilities"]
    )

    details = (
        f"[bold]Name:[/bold] {pokemon['name'.capitalize()]}\n"
        f"[bold]ID:[/bold] {pokemon['id']}\n"
        f"[bold]Type:[/bold] {types}\n"
        f"[bold]Height:[/bold] {pokemon['height'] / 10} m\n"
        f"[bold]Weight:[/bold] {pokemon['weight'] / 10} kg\n"
        f"[bold]Base experience:[/bold] {pokemon['base_experience']}\n"
        f"[bold]Abilities:[/bold] {abilities}"
        #TODO Evolutions
    )

    console.print(Panel(
        details,
        title=f"[bold yellow]{pokemon['name'].capitalize()}[/bold yellow]",
        border_style="green",
        width= 48
    ))

def show_ability_text(pokemon):
    text = []

    for item in pokemon["abilities"]:
        ability = item["ability"]["name"]

        response = requests.get(
            f"{BASE_URL}/ability/{ability}/",
            timeout=TIMEOUT
        )
        response.raise_for_status()
        data = response.json()

        explanation = next(
            (i for i in data["effect_entries"] if i["language"]["name"] == "en"),
            None
        )

        effect = (explanation["short_effect"] if explanation else "No explanation found")

        text.append(f"[bold cyan]{ability}[/bold cyan]\n{effect})")

    console.print(Panel(
        "\n\n".join(text)
    ))



show_ability_text(get_pokemon(3))