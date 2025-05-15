import unittest
from unittest.mock import patch
from requests.status_codes import codes
from gitpy.core.auth import GitPy
from gitpy.core.repos import Repository
from gitpy.exceptions import UnauthorizedError
from gitpy.service.utils import FILLER as F

class TestRepository(unittest.TestCase):

    def setUp(self):
        self.gitpyObj = GitPy("correctusername", "correcttoken")
        self.gitpyObj.network_service = self.gitpyObj.network_service
        self.gitpyObj.user_details = {
            "email" : F.DEFAULT_EMAIL
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
        response = self.repo.create_public_repository("public_repo")
        self.assertEqual(response.status_code,codes.created)
   
    @patch("requests.Session.post")
    def test_create_private_repository(self, mock_post):
        mock_post.return_value.status_code = codes.created
        response = self.repo.create_private_repository("private_repo")
        self.assertEqual(response.status_code,codes.created)

    @patch("requests.Session.get")
    def test_list_repository(self, mock_get):
        mock_get.return_value.status_code = codes.ok
        response = self.repo.list_repositories()
        self.assertEqual(response.status_code,codes.ok)

    @patch("requests.Session.delete")
    def test_delete_repository_success(self, mock_delete):
        mock_delete.return_value.status_code = codes.ok
        response = self.repo.delete_repository("repo-name-that-exists-in-user-account")
        self.assertEqual(response.status_code,codes.ok)

    @patch("requests.Session.delete")
    def test_delete_repository_failure(self, mock_delete):
        mock_delete.return_value.status_code = codes.unauthorized
        with self.assertRaises(UnauthorizedError):
            self.repo.delete_repository("repo-name-that-exists-in-user-account")

    def test_select_repository(self):
        self.repo.select_repository('repo-selected')

    @patch("requests.Session.get")
    def test_get_file(self, mock_get):
        mock_get.return_value.status_code = codes.ok
        response = self.repo.get_file("main.py")
        self.assertEqual(response.status_code,codes.ok)

    @patch("requests.Session.put")
    def test_create_file_success(self,mock_put):
        mock_put.return_value.status_code = codes.created
        response = self.repo.create_file('main.py','import os','file created')
        self.assertEqual(response.status_code,codes.created)

    @patch("requests.Session.put")
    def test_create_file_failed(self,mock_put):
        mock_put.return_value.status_code = codes.unauthorized
        with self.assertRaises(UnauthorizedError):
            self.repo.create_file('main.py','import os','file created')

    @patch("requests.Session.get")
    @patch("requests.Session.put")
    def test_update_file(self,mock_object_get,mock_object_put):
        mock_object_get.return_value.status_code = codes.ok
        mock_object_put.return_value.json.return_value = {
            "sha" : ""
        }
        mock_object_put.return_value.status_code = codes.ok
        response = self.repo.update_file('main.py','import json','updated file')
        self.assertEqual(response.status_code,codes.ok)

    @patch("requests.Session.delete")
    @patch("gitpy.core.repos.Repository.get_file")
    @patch("json.dumps")
    def test_delete_file(self,mock_object_delete,mock_object_get_file,mock_object_json):
        mock_object_delete.return_value.status_code = codes.ok
        mock_object_get_file.return_value.status_code = codes.ok
        mock_object_get_file.json = {
            "sha" : ""
        }
        mock_object_json.return_value.status_code = codes.ok
        response = self.repo.delete_file('main.py','updated file')
        self.assertEqual(response.status_code,codes.ok)

    @patch("requests.Session.put")
    @patch("gitpy.core.repos.Repository.get_file")
    @patch("gitpy.core.repos.Repository.create_file")
    def test_rename_file(self,mock_object_put,mock_object_get_file,mock_object_create_file):      
        mock_object_put.return_value.status_code = codes.ok
        mock_object_get_file.return_value.json = {
            "sha" : "",
            "content" : ""
        }
        mock_object_get_file.return_value.status_code = codes.ok
        mock_object_create_file.return_value.status_code = codes.ok
        mock_object_get_file.return_value = ""
        self.repo.rename_file('main.py','updated file')

    @patch("requests.Session.get")
    def test_login_required_failed(self, mock_get):
        self.gitpyObj.user_details = None
        mock_get.return_value.status_code = codes.ok
        with self.assertRaises(UnauthorizedError):
            self.repo.list_repositories()
