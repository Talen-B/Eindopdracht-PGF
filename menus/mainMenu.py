from rich.console import Console

from menus import searchMenu, teamMenu
from menus.menuTemplate import show_menu

console = Console()

def show_main(user_manager):
    while True:
        choice = show_menu(
            "Main Menu",
            ["View account", "View Teams", "Browse Pokémon", "Log out"]
        )
        match choice:
            case 1:
                show_account(user_manager)
            case 2:
                teamMenu.show_team_menu(user_manager)
            case 3:
                searchMenu.show_pokemon_search(user_manager)
            case 4:
                user_manager.logout()
                return

def show_account(user_manager):
    user = user_manager.current_user
    choice = show_menu(
        f"{user.username}",
        ["Change Username", "View Teams", "Back to menu"]
    )