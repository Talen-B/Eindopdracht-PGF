import User
import json

class UserManager:
    def __init__(self):
        self.users = {}
        try:
            with open("users.json", "r") as f:
                users_data = json.load(f)

            for username, user_data in users_data.items():
                self.users[username] = User.User(
                    user_data["username"],
                    user_data["password"]
                )

        except (FileNotFoundError, json.JSONDecodeError):
            self.users = {}

    def save_users(self):
        data = {}
        for username, user in self.users.items():
            data[username] = user.to_dict()

        with open("users.json", "w") as f:
            json.dump(data, f, indent=4)

    def new_user(self, username, password):
        if username in self.users:
            return

        user = User.User(username, password)
        self.users[username] = user

        self.save_users()

