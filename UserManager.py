import User
import json
import logging

logger = logging.getLogger(__name__)

class UserManager:
    """
    Manages user data

    Can have the following returns:
    SUCCESS, FULL, ALREADY_EXISTS, INVALID_CREDENTIALS, PASSWORD_NOT_NEW
    """
    SUCCESS = "success"
    FULL = "full"
    ALREADY_EXISTS = "already_exists"
    INVALID_CREDENTIALS = "invalid_credentials"
    PASSWORD_NOT_NEW = "password_not_new"

    def __init__(self):
        self.current_user = None
        self.users = {}
        try:
            with open("users.json", "r") as f:
                users_data = json.load(f)

            for username, user_data in users_data.items():
                self.users[username] = User.User(
                    user_data["username"],
                    user_data["password"],
                    user_data["teams"]
                )

        except (FileNotFoundError, json.JSONDecodeError):
            self.users = {}

    def save_users(self):
        """
        Writes all users and data to users.json
        :return:
        """
        data = {}
        for username, user in self.users.items():
            data[username] = user.to_dict()

        with open("users.json", "w") as f:
            json.dump(data, f, indent=4)

    def new_user(self, username, password):
        if username in self.users:
            logger.warning("Username %s already exists", username)
            return self.ALREADY_EXISTS
        user = User.User(username, password, teams={})
        self.users[username] = user
        self.save_users()

        logger.info("User %s registered", username)
        return self.SUCCESS

    def login(self, username, password):
        """
        Sets current_user to user if successful
        :param username:
        :param password:
        :return:
        """
        user = self.users.get(username)

        if user is None or user.password != password:
            logger.warning("Failed login attempt for user %s", username)
            return self.INVALID_CREDENTIALS

        self.current_user = user
        logger.info("User %s successfully logged in", username)
        return self.SUCCESS

    def update_username(self, old_username, new_username):
        if new_username in self.users:
            logger.warning("Username %s already exists", new_username)
            return self.ALREADY_EXISTS
        user = self.users.pop(old_username)

        user.username = new_username

        self.users[new_username] = user

        self.save_users()
        logger.info(
            "Username changed from %s to %s",
            old_username, new_username
        )
        return self.SUCCESS

    def update_password(self, new_password):
        old_password = self.current_user.password
        if old_password == new_password:
            return self.PASSWORD_NOT_NEW
        self.current_user.password = new_password
        self.save_users()
        logger.info("Password successfully changed for user %s",self.current_user.username)
        return self.SUCCESS

    def logout(self):
        """
        Sets current_user to None
        :return:
        """
        username = self.current_user.username
        self.current_user = None
        logger.info("User %s logged out", username)

    def new_team(self, team_name):
        if team_name in self.current_user.teams:
             return self.ALREADY_EXISTS

        self.current_user.teams[team_name] = {"pokemon": {}}
        self.save_users()
        logger.info(
            "User %s created team %s",
            self.current_user.username, team_name
        )
        return self.SUCCESS

    def delete_team(self, team_name):
        del self.current_user.teams[team_name]

        self.save_users()

        logger.info(
            "User %s deleted team %s",
            self.current_user.username, team_name
        )

        return self.SUCCESS

    def add_pokemon(self, pokemon, team_name):
        pokemon_id = str(pokemon["id"])
        pokemon_team = self.current_user.teams[team_name]["pokemon"]

        if pokemon_id in pokemon_team:
            return self.ALREADY_EXISTS
        elif len(pokemon_team.keys()) == 6:
            return self.FULL

        pokemon_team.update({
            pokemon_id: {
                "name" : pokemon["name"]
            }
        })
        self.save_users()
        logger.info(
            "Pokemon %s added to team %s by user: %s",
            pokemon["name"], team_name, self.current_user
        )
        return self.SUCCESS

    def delete_pokemon(self, pokemon, team_name):
        pokemon_id = str(pokemon["id"])
        del self.current_user.teams[team_name]["pokemon"][pokemon_id]
        self.save_users()
        logger.info(
            "Pokemon %s released from team %s by user: %s",
            pokemon["name"], team_name, self.current_user
        )
        return self.SUCCESS