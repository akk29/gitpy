import requests, logging
from gitpy.service.networkService import NetworkService
from gitpy.utils.urls import AUTHENTICATION_URLS , generate_url
from gitpy.utils.log import LOGGING_MSGS

logger = logging.getLogger(__name__)
class GitPy:

    def __init__(self, username=None, token=None):
        self.username = username
        self.token = token
        self.network_service = NetworkService(
            headers={"Authorization": "Token {}".format(self.token)}
        )

    def authenticate(self):
        payload = {"username": self.username}
        url = generate_url(AUTHENTICATION_URLS.USER,payload)
        logging.info(LOGGING_MSGS.AUTH_START)
        try:
            response = self.network_service.get(url)
            logging.info(LOGGING_MSGS.AUTH_SUCCESS)
            return response
        except requests.exceptions.RequestException as err:
            logging.error(LOGGING_MSGS.AUTH_ERROR + repr(err))