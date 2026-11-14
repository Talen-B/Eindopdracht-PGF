from rich.console import Console

from UserManager import UserManager
from menus.menuTemplate import show_menu
from pokemon_api import *

console = Console(force_terminal=True, legacy_windows=False, highlight=False)

def show_pokemon_search(user_manager):
    while True:
        choice = show_menu(
            "Browse Pokémon",
            ["Search by name", "Back"]
        )
        match choice:
            case 1:
                pokemon = search_pokemon()
                if pokemon is None:
                    continue
                if pokemon is not None:
                    show_data_menu(pokemon, user_manager)
                continue
            case 2:
                return

def show_data_menu(pokemon, user_manager):
    while True:
        choice = show_menu(
            pokemon["name"].capitalize(),
            ["Type effectiveness", "Explain Abilities", "Add to team", "Back"],
            body=pokemon_details(pokemon),
        )
        match choice:
            case 1:
                show_type_effectiveness(pokemon["name"])
            case 2:
                show_ability_text(pokemon)
            case 3:
                add_to_team_menu(pokemon, user_manager)
            case 4:
                return

def add_to_team_menu(pokemon, user_manager):
    user = user_manager.current_user
    pokemon_name = pokemon["name"].capitalize()

    while True:
        if not bool(user.teams):
            console.print(f"[bold red]Please make a team before adding Pokémon.\n[/bold red]")
            break

        options = [*user.teams.keys(), "Back"]
        choice = show_menu(
            f"{user.username}'s Teams",
            options,
            body="Which team do you want to add the Pokémon to?"
        )
        if choice == len(options):
            return
        elif choice != type(int):
            continue
        else:
            while True:
                team_name = options[choice - 1]
                result = user_manager.add_pokemon(pokemon, team_name)

                if result == UserManager.FULL:
                    console.print(f"[bold red]Failed to add {pokemon_name} to {team_name}\nTeam is full![/bold red]")
                    break
                elif result == UserManager.ALREADY_EXISTS:
                    console.print(f"[bold red]Failed to add {pokemon_name} to {team_name}\nCan't have duplicate Pokémon in a team![/bold red]")
                    break
                elif result == UserManager.SUCCESS:
                    console.print(f"[bold cyan]{pokemon_name} successfully added to {team_name}![/bold cyan]")
                    break
                else:
                    console.print(f"[bold red]Failed to add {pokemon_name} to {team_name}\n[/bold red]")
                    break
