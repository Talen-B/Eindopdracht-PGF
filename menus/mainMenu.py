from rich.console import Console

from UserManager import UserManager
from menus import searchMenu, teamMenu, menuTemplate
from menus.menuTemplate import show_menu
console = menuTemplate.console

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
    while True:
        user = user_manager.current_user
        choice = show_menu(
            f"{user.username}",
            ["Change username", "Change password", "Back"]
        )
        match choice:
            case 1:
                change_username(user_manager,user)
            case 2:
                change_password(user_manager)
            case 3:
                return


def change_username(user_manager,user):
    while True:
        console.print("[dim]Type 0 to cancel.[/dim]")
        new_username = input("New username: ")
        if new_username == "0":
            return
        result = user_manager.update_username(user.username, new_username)
        if result == UserManager.ALREADY_EXISTS:
            console.print("[red]Username already exists, try again.[/red]")
            continue
        elif result == UserManager.SUCCESS:
            console.print("[green]Name successfully updated![/green]")
            return

def change_password(user_manager):
    while True:
        console.print("[dim]Type 0 to cancel.[/dim]")
        new_password = input("New password: ")
        if new_password == "0":
            return
        confirm_password = input("Confirm password: ")
        if new_password != confirm_password:
            console.print("[red]Passwords do not match, try again[/red]")
            continue
        result = user_manager.update_password(new_password)
        if result == UserManager.PASSWORD_NOT_NEW:
            console.print("[red]Password cannot be the same as old password, try again.[/red]")
            continue
        elif result == UserManager.SUCCESS:
            console.print("[green]Password successfully updated![/green]")
            return