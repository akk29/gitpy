import json, requests
from requests.status_codes import codes
from gitpy.service.loggerService import Logger
from gitpy.exceptions import RequestLibraryWarning, RequestLibraryError, error_handler

class NetworkService:

    def __init__(self, headers=None):
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.logger = Logger.get_logger()

    def request_handler(self,err):
        if(isinstance(err,requests.exceptions.RequestException)):
            self.logger.error(f'request exception - {err.__repr__()}')
            raise RequestLibraryError()
        if(isinstance(err,requests.exceptions.RequestsWarning)):
            self.logger.warning(f'request warning - {err.__repr__()}')
            raise RequestLibraryWarning()
        response = err.args[0]
        error_handler(response.status_code,response)


    def get(self, url):
        try:
            response = self.session.get(url)
            if(response.status_code >= codes.bad_request):
                raise Exception(response)
            return response
        except Exception as err:
            self.request_handler(err)
    
    def post(self, url, payload):
        try:
            response = self.session.post(url, data=json.dumps(payload))
            if(response.status_code >= codes.bad_request):
                raise Exception(response)
            return response
        except Exception as err:
            self.request_handler(err)

    def delete(self, url,payload=None):
        try:
            if(payload):
                response = self.session.delete(url, data=json.dumps(payload))
            else:
                response = self.session.delete(url)
            if(response.status_code >= codes.bad_request):
                raise Exception(response)
            return response
        except Exception as err:
            self.request_handler(err)

    def update(self, url, payload):
        try:
            response = self.session.put(url, data=json.dumps(payload))
            if(response.status_code >= codes.bad_request):
                raise Exception(response)
            return response
        except Exception as err:
            self.request_handler(err)