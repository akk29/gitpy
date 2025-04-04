from gitpy.utils.urls import generate_url, REPOSITORY_URLS
import requests, logging

logger = logging.getLogger(__name__)
class Repository:

    def __init__(self, authenticated_obj):
        self.gitpy_obj = authenticated_obj
        self.network_service = self.gitpy_obj.network_service

    def list_all_user_repositories(self):
        """List all the repositories of User https://api.github.com/:user/repos"""
        url = generate_url(REPOSITORY_URLS.LIST_REPOS,{})
        logging.info("Started listing all repositories")
        try:
            response = self.network_service.get(url)
            logging.info("Completed listing all repositories")
            return response
        except requests.exceptions.RequestException as err:
            logging.error('Issue with listing all user repo' + repr(err))

    def __create_post_data(self, repo_name, access=None):
        """https://developer.github.com/v3/repos/#create"""
        repo_meta_data = {
            "name": "{}".format(repo_name),
            "description": "",
            "homepage": "",
            "has_issues": True,
            "has_projects": True,
            "has_wiki": True,
        }
        if access:  # for private repo
            repo_meta_data["private"] = True
        return repo_meta_data

    def create_repository(self, repo_name, access):
        """Creating repository"""
        payload = self.__create_post_data(repo_name, access)
        url = generate_url(REPOSITORY_URLS.CREATE_REPO,{})
        logging.info("Started creating repositories")
        try:
            response = self.network_service.post(url, payload)
            logging.info("Completed creating repositories")
            return response
        except requests.exceptions.RequestException as err:
            logging.error('Issue with listing all user repositories' + repr(err))

    def create_public_repository(self, repo_name):
        return self.create_repository(repo_name, False)

    def create_private_repository(self, repo_name):
        return self.create_repository(repo_name, True)

    def delete_repository(self, repo_name):
        params = {"username": self.gitpy_obj.username, "repo_name": repo_name}
        url = generate_url(REPOSITORY_URLS.REPO_URL,params)
        logging.info("Started deleting repository")
        try:
            response = self.network_service.delete(url)
            logging.info("Completed deleting repository")
            return response
        except requests.exceptions.RequestException as err:
            logging.error('Issue with deleting repositories' + repr(err))
