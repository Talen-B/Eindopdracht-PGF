class User:
    def __init__(self, username, password, teams):
        self.username = username
        self.password = password
        self.teams = teams

    def __str__(self):
        return f"Username: {self.username}"

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "teams": self.teams
        }
