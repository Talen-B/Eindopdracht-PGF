import requests

from UserManager import UserManager
from menus import MainMenu


def get_pokemon(url_id):
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{url_id}/"
    response = requests.get(pokemon_url)

    data = response.json()

    print(data["name"])

def main():
    user_manager = UserManager()
    user_manager.new_user("Bem", "eonaoevnaeoinvioae")
    MainMenu.show()

main()
