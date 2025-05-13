import unittest
from unittest.mock import patch
from gitpy.core.auth import GitPy
from gitpy.core.repos import Repository
from gitpy.service.utils import DEFAULT_EMAIL
from gitpy.exceptions import UnauthorizedError
from requests.status_codes import codes

class TestRepository(unittest.TestCase):

    def setUp(self):
        self.gitpyObj = GitPy("correctusername", "correcttoken")
        self.gitpyObj.network_service = self.gitpyObj.network_service
        self.gitpyObj.user_details = {
            "email" : DEFAULT_EMAIL
        }
        self.repo = Repository(self.gitpyObj)
    
    @patch("requests.Session.post")
    def test_create_repository_success(self, mock_post):
        mock_post.return_value.status_code = codes.created
        self.repo.create_repository("public_repo",False)
        response = self.repo.create_repository("private_repo",True)
        self.assertEqual(response.status_code,codes.created)

    @patch("requests.Session.post")
    def test_create_repository_failed(self, mock_post):
        mock_post.return_value.status_code = codes.unauthorized
        mock_post.return_value.json.return_value = {}
        with self.assertRaises(UnauthorizedError):
            self.repo.create_repository("public_repo",False)
    
    @patch("requests.Session.post")
    def test_create_public_repository(self, mock_post):
        mock_post.return_value.status_code = codes.created
        self.repo.create_public_repository("public_repo")
   
    @patch("requests.Session.post")
    def test_create_private_repository(self, mock_post):
        mock_post.return_value.status_code = codes.created
        self.repo.create_private_repository("private_repo")

    @patch("requests.Session.get")
    def test_list_repository(self, mock_get):
        mock_get.return_value.status_code = 200
        self.repo.list_repositories()

    @patch("requests.Session.delete")
    def test_delete_repository_success(self, mock_delete):
        mock_delete.return_value.status_code = 200
        self.repo.delete_repository("repo-name-that-exists-in-user-account")

    @patch("requests.Session.delete")
    def test_delete_repository_failure(self, mock_delete):
        mock_delete.return_value.status_code = codes.unauthorized
        with self.assertRaises(UnauthorizedError):
            self.repo.delete_repository("repo-name-that-exists-in-user-account")

    def test_select_repository(self):
        self.repo.select_repository('repo-selected')

    @patch("requests.Session.get")
    def test_get_file(self, mock_get):
        mock_get.return_value.status_code = 200
        self.repo.get_file("main.py")

    @patch("requests.Session.put")
    def test_create_file_success(self,mock_put):
        mock_put.return_value.status_code = 200
        self.repo.create_file('main.py','import os','file created')

    @patch("requests.Session.put")
    def test_create_file_failed(self,mock_put):
        mock_put.return_value.status_code = codes.unauthorized
        with self.assertRaises(UnauthorizedError):
            self.repo.create_file('main.py','import os','file created')

    @patch("requests.Session.get")
    @patch("requests.Session.put")
    def test_update_file(self,mock_object_get,mock_object_put):
        mock_object_get.return_value.status_code = 200
        mock_object_put.return_value.json.return_value = {
            "sha" : ""
        }
        mock_object_put.return_value.status_code = 200
        self.repo.update_file('main.py','import json','updated file')

    # @patch("requests.Session.delete")
    # @patch("gitpy.core.repos.Repository.get_file")
    # def test_delete_file(self,mock_object_delete,mock_object_get_file):
    #     mock_object_delete.return_value.status_code = 200
    #     mock_object_get_file.return_value.status_code = 200
    #     mock_object_get_file.return_value.json.return_value = {
    #         "sha" : ""
    #     }
    #     self.repo.delete_file('main.py','updated file')

    # @patch("requests.Session.delete")
    # @patch("gitpy.core.repos.Repository.get_file")
    # @patch("gitpy.core.repos.Repository.create_file")
    # @patch("gitpy.core.repos.Repository.delete_file")
    # def test_rename_file(self,mock_object_one,mock_object_two,mock_object_three,mock_object_four):        
    #     self.repo.rename_file('main.py','updated file')

    # @patch("requests.Session.get")
    # @patch("requests.Session.post")
    # @patch("requests.Session.delete")
    # def test_rename_file(self,mock_object_get,mock_object_post,mock_object_delete):      
    #     mock_object_get.return_value.status_code = 200
    #     mock_object_get.return_value.json.return_value = {
    #         "sha" : "",
    #         "content" : b"cHl0aG9u"
    #     } 
    #     mock_object_post.return_value.status_code = 200
    #     mock_object_delete.return_value.status_code = 200
    #     self.repo.rename_file('main.py','updated file')

    @patch("requests.Session.delete")
    @patch("gitpy.core.repos.Repository.get_file")
    def test_delete_file(self,mock_object_one,mock_object_two):
        mock_object_one.return_value.status_code = 200
        mock_object_two.return_value.status_code = 200
        mock_object_two.return_value.json.return_value = {
            "sha" : ""
        }
        self.repo.delete_file('main.py','updated file')