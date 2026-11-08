import requests
from rich.panel import Panel

from menus import menuTemplate

console = menuTemplate.console
BASE_URL = "https://pokeapi.co/api/v2"
TIMEOUT = 10

def get_pokemon(name):
    url = f"{BASE_URL}/pokemon/{name}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()


    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print("Pokémon not found!")
        else:
            print(f"HTTP error: {e}")

        return None

    except requests.exceptions.RequestException as e:
        print(f"API connection error: {e}")
        return None

def search_pokemon():
    while True:
        name = input("What Pokémon are you looking for?: ")
        pokemon = get_pokemon(name)

        if pokemon is not None:
            return pokemon

        console.print("[bold red]Pokémon not found! Try again.[/bold red]")
        return None

def pokemon_details(pokemon):
    types = ", ".join(
        item["type"]["name"].capitalize()
        for item in pokemon["types"]
    )

    abilities = ", ".join(
        item["ability"]["name"].replace("-", " ").title()
        for item in pokemon["abilities"]
    )

    details = (
        f"[bold]Name:[/bold] {pokemon['name'].capitalize()}\n"
        f"[bold]ID:[/bold] {pokemon['id']}\n"
        f"[bold]Type:[/bold] {types}\n"
        f"[bold]Height:[/bold] {pokemon['height'] / 10} m\n"
        f"[bold]Weight:[/bold] {pokemon['weight'] / 10} kg\n"
        f"[bold]Base experience:[/bold] {pokemon['base_experience']}\n"
        f"[bold]Abilities:[/bold] {abilities}"
        #TODO Evolutions
    )

    return details

def show_pokemon(pokemon):
    console.print(Panel(
        pokemon_details(pokemon),
        title=f"[bold yellow]{pokemon['name'].capitalize()}[/bold yellow]",
        border_style="green",
        width=48,
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

        effect = explanation["short_effect"] if explanation else "No explanation found"

        text.append(f"[bold cyan]{ability.capitalize()}[/bold cyan]\n{effect}")

    console.print(Panel(
        "\n\n".join(text) or "No abilities listed.",
        title = f"[bold yellow]{pokemon["name"].capitalize()} Abilities[/bold yellow]",
        border_style = "green",
        width = 48,
    ), "[dim]Press [Enter] to continue.[/dim]")
    input()

