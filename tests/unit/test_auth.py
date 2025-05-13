import unittest
from unittest.mock import patch
from requests.status_codes import codes
from gitpy.core.auth import GitPy
from gitpy.exceptions import UnauthorizedError
class TestAuth(unittest.TestCase):

    def setUp(self):
        self.gitpy_obj = GitPy("correctusername", "correcttoken")

    @patch("requests.Session.get")
    def test_authentication_success(self, mock_get):
        mock_get.return_value.status_code = 200
        response = self.gitpy_obj.authenticate()
        self.assertEqual(response.status_code, 200)

    @patch("requests.Session.get")
    def test_authentication_failed(self, mock_get):
        mock_get.return_value.status_code = 401
        mock_get.return_value.json.return_value = {}
        with self.assertRaises(UnauthorizedError):
            self.gitpy_obj.authenticate()