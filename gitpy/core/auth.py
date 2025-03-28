import requests
from gitpy.service.networkService import NetworkService
from gitpy.constants.urls import AUTHENTICATION_URLS , generate_url


class GitPy:

    def __init__(self, username=None, token=None):
        self.username = username
        self.token = token
        self.network_service = NetworkService(
            headers={"Authorization": "Token {}".format(self.token)}
        )

    def authenticate(self):
        payload = {"username": self.username}
        url = generate_url(AUTHENTICATION_URLS.USER,payload)
        try:
            response = self.network_service.get(url)
            return response
        except requests.exceptions:
            return requests.exceptions
