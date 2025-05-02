import unittest
from unittest.mock import patch
from gitpy.core.auth import GitPy

class TestAuth(unittest.TestCase):

    def setUp(self):
        self.gitpy_obj = g = GitPy("correctusername", "correcttoken")

    @patch("gitpy.service.networkService.NetworkService.get")
    def test_authentication_success(self, mock_object):
        self.gitpy_obj.authenticate()

if __name__ == "__main__":
    unittest.main()
