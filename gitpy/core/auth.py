from collections import defaultdict
from gitpy.service.networkService import NetworkService
from gitpy.service.urls import AUTHENTICATION_URLS , generate_url
from gitpy.service.utils import FILLER as F
class GitPy:

    def __init__(self, username=None, token=None):
        self.username = username
        self.token = token
        self.network_service = NetworkService(
            headers={
                F.AUTHORIZATION : "Bearer {}".format(self.token), 
                F.X_GITHUB_API_VERSION : F.GITHUB_CURRENT_VERSION, 
                F.ACCEPT: F.APPLICATION_JSON, 
                F.USER_AGENT : F.AWESOME_OCTOCAT_APP }
        )
        self.user_details = None

    def authenticate(self):
        '''https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#get-the-authenticated-user'''
        url = generate_url(AUTHENTICATION_URLS.USER,{})
        response = self.network_service.get(url)
        self.user_details = defaultdict(lambda : None,response.json())
        return response
    
    def get_user_details(self):
        return self.user_details