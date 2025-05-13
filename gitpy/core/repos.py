import base64
from gitpy.service.urls import generate_url, REPOSITORY_URLS
from gitpy.service.utils import DEFAULT_EMAIL,FILE_CREATED_FOR_RENAME_OPERATION,FILE_DELETED_FOR_RENAME_OPERATION

class Repository:

    '''https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28'''

    def __init__(self, authenticated_obj):
        self.gitpy_obj = authenticated_obj
        self.network_service = self.gitpy_obj.network_service
        self._current_repository = None
        self._current_branch = None

    def list_repositories(self):
        """https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-organization-repositories"""
        url = generate_url(REPOSITORY_URLS.LIST_REPOS,{})
        return self.network_service.get(url)

    def __create_post_data(self, repo_name, access=None):
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
        """https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#create-an-organization-repository"""
        payload = self.__create_post_data(repo_name, access)
        url = generate_url(REPOSITORY_URLS.CREATE_REPO,{})
        response = self.network_service.post(url, payload)
        self.select_repository(repo_name)
        return response

    def create_public_repository(self, repo_name):
        return self.create_repository(repo_name, False)

    def create_private_repository(self, repo_name):
        return self.create_repository(repo_name, True)

    def delete_repository(self, repo_name):
        '''https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#delete-a-repository'''
        params = {"username": self.gitpy_obj.username, "repo_name": repo_name}
        url = generate_url(REPOSITORY_URLS.REPO_URL,params)
        return self.network_service.delete(url,None)
    
    def select_repository(self,repo_name):
        self._current_repository = repo_name

    def create_file(self,abs_path,content,msg):
        '''https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#create-or-update-file-contents'''
        params = {"owner" : self.gitpy_obj.username, "repo" : self._current_repository, "path" : abs_path}
        url = generate_url(REPOSITORY_URLS.CREATE_FILE,params)
        payload = {
            "message" : msg,
            "committer" : {
                "name" : self.gitpy_obj.username,
                "email" : DEFAULT_EMAIL if not self.gitpy_obj.user_details['email'] else self.gitpy_obj.user_details['email']
            },
            "content" : base64.b64encode(bytes(content,"utf-8")).decode('utf-8')
        }
        return self.network_service.update(url,payload)

    def get_file(self,abs_path):
        '''https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#get-repository-content'''
        params = {"owner" : self.gitpy_obj.username, "repo" : self._current_repository, "path" : abs_path}
        url = generate_url(REPOSITORY_URLS.GET_FILE,params)
        return self.network_service.get(url)

    def update_file(self,abs_path,content,msg):
        '''https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#create-or-update-file-contents'''
        file_details = self.get_file(abs_path)
        if(file_details):
            _sha = file_details.json()['sha'] 
            payload = {
                "message" : msg,
                "committer" : {
                    "name" : self.gitpy_obj.username,
                    "email" : DEFAULT_EMAIL if not self.gitpy_obj.user_details['email'] else self.gitpy_obj.user_details['email']
                },
                "sha": _sha,
                "content" : base64.b64encode(bytes(content,"utf-8")).decode('utf-8')
            }
            params = {"owner" : self.gitpy_obj.username, "repo" : self._current_repository, "path" : abs_path}
            url = generate_url(REPOSITORY_URLS.UDPATE_FILE,params)
            return self.network_service.update(url,payload)

    def delete_file(self,abs_path,msg):
        '''https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#delete-a-file'''
        file_details = self.get_file(abs_path)
        if(file_details):
            _sha = file_details.json()['sha'] 
            payload = {
                "message" : msg,
                "committer" : {
                    "name" : self.gitpy_obj.username,
                    "email" : DEFAULT_EMAIL if not self.gitpy_obj.user_details['email'] else self.gitpy_obj.user_details['email']
                },
                "sha": _sha
            }
            params = {"owner" : self.gitpy_obj.username, "repo" : self._current_repository, "path" : abs_path}
            url = generate_url(REPOSITORY_URLS.DELETE_FILE,params)
            return self.network_service.delete(url,payload)

    def rename_file(self,current,_new):
        ''' WARNING: GitHub REST API doesn't support rename file operation
            Hence to do it we need to create the new file with old content
            and delete the old file
            resulting in two commit operation
        '''
        file_details = self.get_file(current)
        if(file_details):
            content = file_details.json()['content']
            self.create_file(_new,content,FILE_CREATED_FOR_RENAME_OPERATION)
            self.delete_file(current,FILE_DELETED_FOR_RENAME_OPERATION)        
