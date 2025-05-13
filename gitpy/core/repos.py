import base64
from gitpy.service.urls import generate_url, REPOSITORY_URLS
from gitpy.service.utils import FILLER as F

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
            F.NAME: "{}".format(repo_name),
            F.DESCRIPTION: "",
            F.HOME_PAGE: "",
            F.HAS_ISSUES: True,
            F.HAS_PROJECTS: True,
            F.HAS_WIKI: True,
        }
        if access:  # for private repo
            repo_meta_data[F.PRIVATE] = True
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
        params = {F.USERNAME: self.gitpy_obj.username, F.REPO_NAME: repo_name}
        url = generate_url(REPOSITORY_URLS.REPO_URL,params)
        return self.network_service.delete(url,None)
    
    def select_repository(self,repo_name):
        self._current_repository = repo_name

    def create_file(self,abs_path,content,msg):
        '''https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#create-or-update-file-contents'''
        params = {F.OWNER : self.gitpy_obj.username, F.REPO : self._current_repository, F.PATH : abs_path}
        url = generate_url(REPOSITORY_URLS.CREATE_FILE,params)
        payload = {
            F.MESSAGE: msg,
            F.COMMITTER : {
                F.NAME : self.gitpy_obj.username,
                F.EMAIL : F.DEFAULT_EMAIL if not self.gitpy_obj.user_details[F.EMAIL] else self.gitpy_obj.user_details[F.EMAIL]
            },
            F.CONTENT : base64.b64encode(bytes(content,F.UTF8)).decode(F.UTF8)
        }
        return self.network_service.update(url,payload)

    def get_file(self,abs_path):
        '''https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#get-repository-content'''
        params = {F.OWNER: self.gitpy_obj.username, F.REPO : self._current_repository, F.PATH : abs_path}
        url = generate_url(REPOSITORY_URLS.GET_FILE,params)
        return self.network_service.get(url)

    def update_file(self,abs_path,content,msg):
        '''https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#create-or-update-file-contents'''
        file_details = self.get_file(abs_path)
        if(file_details):
            _sha = file_details.json()[F.SHA] 
            payload = {
                F.MESSAGE : msg,
                F.COMMITTER : {
                    F.NAME : self.gitpy_obj.username,
                    F.EMAIL : F.DEFAULT_EMAIL if not self.gitpy_obj.user_details[F.EMAIL] else self.gitpy_obj.user_details[F.EMAIL]
                },
                F.SHA: _sha,
                F.CONTENT : base64.b64encode(bytes(content,F.UTF8)).decode(F.UTF8)
            }
            params = {F.OWNER: self.gitpy_obj.username, F.REPO : self._current_repository, F.PATH : abs_path}
            url = generate_url(REPOSITORY_URLS.UDPATE_FILE,params)
            return self.network_service.update(url,payload)

    def delete_file(self,abs_path,msg):
        '''https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#delete-a-file'''
        file_details = self.get_file(abs_path)
        if(file_details):
            _sha = file_details.json()[F.SHA] 
            payload = {
                F.MESSAGE : msg,
                F.COMMITTER : {
                    F.NAME : self.gitpy_obj.username,
                    F.EMAIL : F.DEFAULT_EMAIL if not self.gitpy_obj.user_details[F.EMAIL] else self.gitpy_obj.user_details[F.EMAIL]
                },
                F.SHA: _sha
            }
            params = {F.OWNER : self.gitpy_obj.username, F.REPO : self._current_repository, F.PATH : abs_path}
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
            content = file_details.json()[F.CONTENT]
            self.create_file(_new,content,F.FILE_CREATED_FOR_RENAME_OPERATION)
            self.delete_file(current,F.FILE_DELETED_FOR_RENAME_OPERATION)        
