from rich.console import Console

from menus.menuTemplate import show_menu
from pokemon_api import *

console = Console()

def show_pokemon_search(user_manager):
    while True:
        choice = show_menu(
            "Browse Pokémon",
            ["Search by name", "Search by type", "Back"]
        )
        match choice:
            case 1:
                pokemon = search_pokemon()
                if pokemon is not None:
                    show_data_menu(pokemon, user_manager)
                return
            case 2:
                pass
            case 3:
                return

def show_data_menu(pokemon, user_manager):
    while True:
        choice = show_menu(
            pokemon["name"].capitalize(),
            ["Explain Abilities", "Add to team", "Back"],
            body=pokemon_details(pokemon),
        )
        match choice:
            case 1:
                show_ability_text(pokemon)
            case 2:
                add_to_team_menu(pokemon, user_manager)
                return
            case 3:
                return

def add_to_team_menu(pokemon, user_manager):
    user = user_manager.current_user

    while True:
        options = [*user.teams.keys(), "Back"]
        choice = show_menu(
            f"{user.username}'s Teams",
            options,
            body="Which team do you want to add the Pokémon to?"
        )
        if choice == len(options):
            return
        else:
            team_name = options[choice - 1]
            result = user_manager.add_pokemon(pokemon, team_name)
            pokemon_name = pokemon["name"].capitalize()

            if result == "Full":
                console.print(f"[bold red]Failed to add {pokemon_name} to {team_name}\nTeam is full![/bold red]")
                return
            elif result:
                console.print(f"[bold cyan]{pokemon_name} successfully added to {team_name}![/bold cyan]")
                return
            else:
                console.print(f"[bold red]Failed to add {pokemon_name} to {team_name}\n[/bold red]")
                return
