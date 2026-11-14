import requests
from rich.panel import Panel

from menus import menuTemplate

console = menuTemplate.console
BASE_URL = "https://pokeapi.co/api/v2"
TIMEOUT = 10

def get_api_data(url, item_name):
    """
    Retrieve data from the PokéAPI and handle request errors.
    :param url:
    :param item_name:
    :return:
    """
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            console.print(f"[bold red]{item_name} not found![/bold red]")
        else:
            console.print(f"[bold red]HTTP error: {e}[/bold red]")

    except requests.exceptions.ConnectionError:
        console.print("[bold red]Could not connect to the PokéAPI![/bold red]")

    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]API request error: {e}[/bold red]")

    return None

def get_pokemon(name):
    """
    Returns pokemon as dict or None if not found.
     Uses name or id as input
    :param name:
    :return dict or None:
    """

    url = f"{BASE_URL}/pokemon/{name}"
    return get_api_data(url, "Pokémon")

def search_pokemon():
    while True:
        console.print("[dim]Type 0 to cancel.[/dim]")
        name = input("What Pokémon are you looking for?: ")
        if name == "0":
            return None
        pokemon = get_pokemon(name)

        if pokemon is not None:
            return pokemon

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

def get_type(type_name):

    url = f"{BASE_URL}/type/{type_name}"
    return get_api_data(url, "Type")



def get_type_effectiveness(pokemon_name):
    """
    Calcs the defensive type effectiveness.
    Returns the effectiveness in a dict.
    Uses endpoint {BASE_URL}/type/{type_name}.

    :param pokemon_name:
    :return dict:
    """
    pokemon = get_pokemon(pokemon_name)

    if pokemon is None:
        return None

    effectiveness= {}
    multipliers = {
        "no_damage_from": 0,
        "half_damage_from": 0.5,
        "double_damage_from": 2
    }

    for pokemon_type in pokemon["types"]:
        type_name = pokemon_type["type"]["name"]
        type_data = get_type(type_name)

        damage_relations = type_data["damage_relations"]
        for relation, multiplier in multipliers.items():
            for attacking_type in damage_relations[relation]:
                attacking_type_name = attacking_type["name"]

                effectiveness[attacking_type_name] = effectiveness.get(attacking_type_name, 1) * multiplier

    return effectiveness

def format_type_effectiveness(effectiveness):
    """
    Uses the effectiveness dict so that I can use it in my menu_template.
    returns the body I can add to my menu.

    :param effectiveness:
    :return (Rich)String:
    """
    weak_to = []
    resists = []
    immune_to = []

    for type_name, multiplier in effectiveness.items():
        if multiplier > 1:
            weak_to.append((type_name, multiplier))
        elif multiplier == 0:
            immune_to.append(type_name)
        elif multiplier < 1:
            resists.append((type_name, multiplier))

    body = "[bold red]Weak to[/bold red]\n"
    if weak_to:
        for name, multiplier in weak_to:
            body += f"  [red]{name.title()} ({multiplier}x)[/red]\n"
    else:
        body += "  None\n"

    body += "\n[bold green]Resists[/bold green]\n"
    if resists:
        for name, multiplier in resists:
            body += f"  [green]{name.title()} ({multiplier}x)[/green]\n"
    else:
        body += "  None\n"

    body += "\n[bold cyan]Immune to[/bold cyan]\n"
    if immune_to:
        for name in immune_to:
            body += f"  [cyan]{name.title()}[/cyan]\n"
    else:
        body += "  None\n"

    return body

def show_type_effectiveness(pokemon_name):
    effectiveness = get_type_effectiveness(pokemon_name)

    if effectiveness is not None:
        while True:
            choice = menuTemplate.show_menu(
                f"{pokemon_name} - Type Effectiveness",
                ["Back"],
                body=format_type_effectiveness(effectiveness)
            )

            if choice == 1:
                break

def show_ability_text(pokemon):
    text = []

    for item in pokemon["abilities"]:
        ability = item["ability"]["name"]

        data = get_api_data(
            f"{BASE_URL}/ability/{ability}/",
            "Ability"
        )
        if data is None:
            text.append(
                f"[bold cyan]{ability.capitalize()}[/bold cyan]\n"
                "Could not retrieve ability description."
            )
            continue

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
