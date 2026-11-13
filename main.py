from UserManager import UserManager
from menus import loginMenu

import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    user_manager = UserManager()
    loginMenu.show_login(user_manager)

main()
