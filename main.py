
from UserManager import UserManager
from menus import loginMenu




def main():
    user_manager = UserManager()
    loginMenu.show_login(user_manager)

main()
