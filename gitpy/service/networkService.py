import requests, json
from requests.status_codes import codes
from gitpy.service.loggerService import Logger
from gitpy.exceptions import ERR_MSG, RequestLibraryWarning, RequestLibraryError, error_handler, FUNCTIONS

class NetworkService:

    def __init__(self, headers=None):
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.logger = Logger.get_logger()

    def request_handler(self,err):
        if(any(isinstance(err, ClassName) for ClassName in [
            requests.exceptions.RequestsWarning, 
            requests.exceptions.FileModeWarning, 
            requests.exceptions.RequestsDependencyWarning])):
            raise RequestLibraryWarning(ERR_MSG.REQUEST_LIBRARY_WARNING)
        else:
            raise RequestLibraryError(ERR_MSG.REQUEST_LIBRARY_ERROR)
        
    def get(self, url):
        try:
            response = self.session.get(url)
            if(response.status_code >= codes.bad_request):
                error_handler(response.status_code,FUNCTIONS.AUTHENICATION,response)
            return response
        except requests.exceptions as err:
            self.request_handler(err)
    
    def post(self, url, payload):
        try:
            response = self.session.post(url, data=json.dumps(payload))
            return response
        except requests.exceptions as err:
            self.request_handler(err)

    def delete(self, url,payload):
        try:
            response = self.session.delete(url, data=json.dumps(payload))
            return response
        except requests.exceptions as err:
            self.request_handler(err)

    def update(self, url, payload):
        try:
            response = self.session.put(url, data=json.dumps(payload))
            return response
        except requests.exceptions as err:
            self.request_handler(err)