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
            return User(id=user["id"], username=user["username"])

        else:
            return None

    def getUser(self, id):
        response = requests.get(url="http://localhost:8080/users/" + id)

        if response.status_code == 200:
            user = response.json()
            return User(id=user["id"], username=user["username"])

        else:
            return None


PRIVATE_API_SERVICE = PrivateApiService()
