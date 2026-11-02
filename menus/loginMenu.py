from rich.prompt import Prompt
from menus import mainMenu
from rich.console import Console
from menus.menuTemplate import show_menu

console = Console()
def show_login(user_manager):
    while True:
        choice = show_menu(
            "Welcome to the Pokémon App!",
            ["Log in", "Register a new account", "Guest account (Wiki only)", "Close the app"]
        )
        match choice:
            case "1":
                username = Prompt.ask("[bold cyan]Username[/bold cyan]")
                password = Prompt.ask("[bold red]Password[/bold red]")
                user = user_manager.login(username, password)
                if user:
                    mainMenu.show_main(user_manager)
                else:
                    console.print("[red]Invalid login.[/red]")
                    continue
            case "2":
                while True:
                    console.print("[dim]Press [Enter] to cancel.[/dim]")
                    username = input("Username: ")
                    if not username:
                        break
                    password =  input("Password: ")
                    new_user = user_manager.new_user(username, password)

                    if new_user == "Username exists":
                        print("Username exists, try again")
                        continue
                    elif new_user:
                        print("Account made! Login to continue.")
                        break
                    else:
                        print("Invalid input")
                        break
            case "3":
                pass #TODO Guest account
            case "4":
                exit()
            case _:
                print("Please enter a valid choice")