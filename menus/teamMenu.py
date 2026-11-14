from rich.prompt import Prompt

from UserManager import UserManager
from menus import searchMenu
from menus.menuTemplate import show_menu, console
from pokemon_api import pokemon_details, show_ability_text, search_pokemon, get_pokemon, show_type_effectiveness


def show_team_menu(user_manager):
    user = user_manager.current_user

    while True:
        options = [*user.teams.keys(), "New Team", "Back"]
        choice = show_menu(
            f"{user.username}'s Teams",
            options,
        )

        if choice == len(options):
            return
        elif choice == len(options) - 1:
            new_team_menu(user_manager)
        elif choice == type(int) and 0 < choice <= len(user.teams.keys()):
            team_name = options[choice - 1]
            edit_team_menu(user, team_name, user_manager)
        else:
            console.print("[bold red]Please enter a valid option.[/bold red]")
            continue


def new_team_menu(user_manager):
    while True:
        console.print("[dim]Type 0 to cancel.[/dim]")
        team_name = Prompt.ask("[bold cyan]What's the team name?[/bold cyan]")
        if team_name == "0":
            return
        team = user_manager.new_team(team_name)
        if team == UserManager.ALREADY_EXISTS:
            console.print("[red]Team name already exists.[/red]")
            continue
        else:
            console.print("[green]Team made! Select to edit.[/green]")
            return

def edit_team_menu(user, team_name, user_manager):
    team = user.teams[team_name]

    while True:
        pokemons = [pokemon["name"].capitalize() for pokemon in team["pokemon"].values()]
        pokemon_amount = len(pokemons)
        options = pokemons + (["Add new pokemon"] if pokemon_amount < 6 else []) + ["Back"]

        choice = show_menu(
            f"{team_name}'s Pokémon",
            options,
            body="Current Pokémon in this team.\n"
                 "Select a Pokémon to edit it.\n"
                 "The max Pokémon is 6."
        )
        if choice == len(options):
            return
        elif pokemon_amount < 6 and choice == len(options) - 1:
            searchMenu.show_pokemon_search(user_manager)
        elif choice == type(int) and 0 < choice <= pokemon_amount:
            pokemon_name = options[choice - 1]
            edit_pokemon_menu(pokemon_name, team_name, user_manager)
        else:
            continue

def edit_pokemon_menu(pokemon_name, team_name, user_manager):
    pokemon = get_pokemon(pokemon_name)
    if pokemon is None:
        console.print("[red]Could not retrieve the current Pokémon data.[/red]")
        return

    while True:
        choice = show_menu(
            f"{pokemon_name}",
            ["Show Pokémon data", "Change Pokémon", "Release Pokémon", "Back"],
            body=f"Current team: {team_name}\nCurrent Pokémon: {pokemon_name}"
        )
        match choice:
            case 1:
                while True:
                    choice = show_menu(
                        pokemon_name,
                        ["Type effectiveness", "Explain Abilities", "Back"],
                        body=pokemon_details(pokemon),
                    )
                    if choice == 1:
                        show_type_effectiveness(pokemon_name)
                    elif choice == 2:
                        show_ability_text(pokemon)
                    elif choice == 3:
                        break
                    else:
                        continue
            case 2:
                while True:
                    choice = show_menu(
                        "Select replacement Pokémon",
                        ["Search by name", "Back"],
                        body=f"Currently replacing: {pokemon_name}"
                    )
                    match choice:
                        case 1:
                            replacement = search_pokemon()
                            if pokemon is None:
                                return
                            if replacement is not None:
                                replace_pokemon_menu(pokemon,replacement, user_manager, team_name)
                        case 2:
                            break
            case 3:
                while True:
                    choice = show_menu(
                        f"Release {pokemon_name}?",
                        ["Yes",  "No, go back"],
                        body="[bold red]This will delete the pokemon from your team[/bold red]\nDo you want to continue?",
                    )
                    if choice == 1:
                        result = user_manager.delete_pokemon(pokemon, team_name)
                        if result == UserManager.SUCCESS:
                            console.print(f"[bold green]{pokemon_name} successfully released.[/bold green]")
                            return
                        else:
                            console.print(f"There was a problem deleting {pokemon_name}.")
                            break
                    elif choice == 2:
                        break
            case 4:
                break

def replace_pokemon_menu(pokemon, replacement, user_manager, team_name):
    replacement_name = replacement["name"]
    pokemon_name = pokemon["name"]
    while True:
        choice = show_menu(
            replacement["name"].capitalize(),
            ["Explain Abilities", f"Use to replace {pokemon_name.capitalize()}", "Back"],
            body=pokemon_details(replacement),
        )
        match choice:
            case 1:
                show_ability_text(pokemon)
            case 2:
                user_manager.delete_pokemon(pokemon, team_name)
                result = user_manager.add_pokemon(replacement, team_name)
                pokemon_name = pokemon["name"].capitalize()
                if result == UserManager.SUCCESS:
                    console.print(f"[bold cyan]{replacement_name} successfully replaced {pokemon_name}![/bold cyan]")
                    return
                else:
                    console.print(f"[bold red]Failed to replace Pokémon\n[/bold red]")
                    return
            case 3:
                return