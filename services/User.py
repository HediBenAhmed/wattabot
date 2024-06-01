from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user):
        self.id = user["id"]
        self.username = user["username"]
        self.features = user["userSettings"]["features"]
