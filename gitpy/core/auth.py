from collections import defaultdict
from gitpy.service.networkService import NetworkService
from gitpy.service.urls import AUTHENTICATION_URLS , generate_url

class GitPy:

    def __init__(self, username=None, token=None):
        self.username = username
        self.token = token
        self.network_service = NetworkService(
            headers={
                "Authorization": "Bearer {}".format(self.token), 
                "X-GitHub-Api-Version" : "2022-11-28", 
                "Accept": "application/vnd.github+json", 
                "User-Agent" : "Awesome-Octocat-App" }
        )
        self.user_details = None

    def authenticate(self):
        '''https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#get-the-authenticated-user'''
        url = generate_url(AUTHENTICATION_URLS.USER,{})
        response = self.network_service.get(url)
        self.user_details = defaultdict(lambda : None,response.json())
        return response