import requests
from services.Service import Service
from services.User import User


class PrivateApiService(Service):

    def login(self, username: str, password: str):
        response = requests.post(
            url="http://localhost:8080/users/login",
            json={"username": username, "password": password},
        )
        print("login", response.status_code, response.json())

        if response.status_code == 200:
            user = response.json()
            return User(user)

        else:
            return None

    def getUser(self, id):
        response = requests.get(url="http://localhost:8080/users/" + id)

        if response.status_code == 200:
            user = response.json()
            return User(user)

        else:
            return None

    def getUserByName(self, username):
        response = requests.post(
            url="http://localhost:8080/users/search",
            json={"username": username},
        )
        print("getUserByName", response.status_code, response.json())

        if response.status_code == 200:
            user = response.json()
            return User(user)

        else:
            return None

    @classmethod
    def createInstance(self):
        return PrivateApiService()
