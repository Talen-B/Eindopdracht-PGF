from rich.console import Console
from menus.menuTemplate import show_menu
from pokemon_api import *

console = Console()

def show_pokemon_search():
    while True:
        choice = show_menu(
            "Browse Pokémon",
            ["Search by name", "Search by type", "Back"]
        )
        match choice:
            case "1":
                pokemon = get_pokemon(input("What pokemon are you looking for?: "))
                show_pokemon(pokemon)
                show_data_menu(pokemon)
            case "2":
                pass
            case "3":

                return

def show_data_menu(pokemon):
    choice = show_menu(
        f"{pokemon["name".capitalize()]} Menu",
        ["Explain Abilities", "Add to team", "Back"]
    )
    match choice:
        case "1":
            show_ability_text(pokemon)