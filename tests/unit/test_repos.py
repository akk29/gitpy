import unittest, base64
from unittest import mock
from unittest.mock import patch
from gitpy.core.repos import Repository
from gitpy.service.utils import DEFAULT_EMAIL

class TestRepository(unittest.TestCase):

    def setUp(self):
        self.gitpyObj = mock.Mock()
        self.gitpyObj.network_service = self.gitpyObj.network_service
        self.gitpyObj.user_details = {
            "email" : DEFAULT_EMAIL
        }
        self.repo = Repository(self.gitpyObj)

    @patch("gitpy.service.networkService.NetworkService.post")
    def test_create_repository(self, mock_object):
        self.repo.create_repository("public_repo",False)
        self.repo.create_repository("private_repo",True)

    @patch("gitpy.service.networkService.NetworkService.post")
    def test_create_public_repository(self, mock_object):
        self.repo.create_public_repository("public_repo")

    @patch("gitpy.service.networkService.NetworkService.post")
    def test_create_private_repository(self, mock_object):
        self.repo.create_private_repository("private_repo")

    @patch("gitpy.service.networkService.NetworkService.get")
    def test_list_repository(self, mock_object):
        self.repo.list_repositories()

    @patch("gitpy.service.networkService.NetworkService.delete")
    def test_delete_repository(self, mock_object):
        self.repo.delete_repository("repo-name-that-exists-in-user-account")

    def test_select_repository(self):
        self.repo.select_repository('repo-selected')

    @patch("gitpy.service.networkService.NetworkService.get")
    def test_get_file(self, mock_object):
        self.repo.get_file("main.py")

    @patch("gitpy.service.networkService.NetworkService.get")
    def test_create_file(self,mock_object):
        self.repo.create_file('main.py','import os','file created')

    @patch("gitpy.service.networkService.NetworkService.update")
    @patch("gitpy.core.repos.Repository.get_file")
    def test_update_file(self,mock_object_one,mock_object_two):
        mock_object_two.json = {
            "sha" : ""
        }
        self.repo.update_file('main.py','import json','updated file')

    @patch("gitpy.service.networkService.NetworkService.delete")
    @patch("gitpy.core.repos.Repository.get_file")
    @patch("gitpy.core.repos.Repository.create_file")
    @patch("gitpy.core.repos.Repository.delete_file")
    def test_rename_file(self,mock_object_one,mock_object_two,mock_object_three,mock_object_four):        
        self.repo.rename_file('main.py','updated file')

    @patch("gitpy.service.networkService.NetworkService.delete")
    @patch("gitpy.core.repos.Repository.get_file")
    def test_delete_file(self,mock_object_one,mock_object_two):
        mock_object_two.json = {
            "sha" : ""
        }
        self.repo.delete_file('main.py','updated file')
