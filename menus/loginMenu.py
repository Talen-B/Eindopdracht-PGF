from rich.prompt import Prompt
from UserManager import UserManager
from menus import mainMenu
from rich.console import Console
from menus.menuTemplate import show_menu

console = Console(force_terminal=True, legacy_windows=False, highlight=False)

def show_login(user_manager):
    while True:
        choice = show_menu(
            "Welcome to the Pokémon App!",
            ["Log in", "Register a new account", "Close the app"]
        )
        match choice:
            case 1:
                username = Prompt.ask("[bold cyan]Username[/bold cyan]")
                password = Prompt.ask("[bold red]Password[/bold red]")
                result = user_manager.login(username, password)
                if result == UserManager.SUCCESS:
                    mainMenu.show_main(user_manager)
                elif result == UserManager.INVALID_CREDENTIALS:
                    console.print("[red]Invalid login.[/red]")
                    continue
            case 2:
                while True:
                    console.print("[dim]Type 0 to cancel.[/dim]")
                    username = input("Username: ")
                    if username == "0":
                        break
                    password =  input("Password: ")
                    new_user = user_manager.new_user(username, password)

                    if new_user == UserManager.ALREADY_EXISTS:
                        print("Username exists, try again")
                        continue
                    elif new_user == UserManager.SUCCESS:
                        print("Account made! Login to continue.")
                        break
                    else:
                        print("Invalid input")
                        break
            case 3:
                exit()