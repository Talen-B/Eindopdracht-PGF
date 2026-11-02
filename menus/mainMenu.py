from rich.console import Console

from menus import searchMenu
from menus.menuTemplate import show_menu

console = Console()

def show_main(user_manager):
    while True:
        choice = show_menu(
            "Main Menu",
            ["View account", "Browse Pokémon", "Log out"]
        )
        match choice:
            case "1":
                show_account(user_manager)
            case "2":
                searchMenu.show_pokemon_search()
            case "3":
                user_manager.logout()
                return

def show_account(user_manager):
    user = user_manager.current_user
    choice = show_menu(
        f"{user.username}",
        ["Change Username", "View Teams", "Back to menu"]
    )