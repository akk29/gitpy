import unittest
from unittest.mock import patch
from gitpy.core.auth import GitPy

class TestAuth(unittest.TestCase):

    def setUp(self):
        self.gitpy_obj = GitPy("correctusername", "correcttoken")

    @patch("requests.Session.get")
    def test_authentication_success(self, mock_object):
        mock_object.return_value.status_code = 200
        self.gitpy_obj.authenticate()

if __name__ == "__main__":
    unittest.main()
