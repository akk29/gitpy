import unittest
from unittest import mock
from unittest.mock import patch
from gitpy.core.repos import Repository

class TestRepository(unittest.TestCase):

    def setUp(self):
        self.gitpyObj = mock.Mock()
        self.gitpyObj.network_service = self.gitpyObj.network_service
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

    @patch("gitpy.service.networkService.NetworkService.get")
    def test_get_file(self, mock_object):
        self.repo.get_file("main.py")
