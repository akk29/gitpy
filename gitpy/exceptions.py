import traceback
from gitpy.service.loggerService import Logger
from requests.status_codes import codes

def process_exception(self):
    tb = traceback.extract_stack()[:-1]  # Exclude current frame        
    last_frame = tb[-4]
    if(hasattr(self,"warning_error")):
        last_frame = tb[-4]
    file_name = last_frame.filename
    line_no = last_frame.lineno
    func_name = last_frame.name
    if(hasattr(self,"warning_error")):
        self.logger.warning(f'{file_name} , {func_name}(), line no : {line_no} , raised {self.__repr__()}')
    else:
        self.logger.error(f'{file_name} , {func_name}(), line no : {line_no} , raised {self.__repr__()} ----- api_response : {self.response}')
class BaseException(IOError):
    
    def __init__(self, *args,**kwargs):
        self.response = kwargs.pop('response')
        self.code = kwargs.pop('code')
        self.logger = Logger.get_logger()
        process_exception(self)
        super().__init__(*args)

class UnauthorizedError(BaseException):
    """Unauthorized Error - 401 Status code"""

class ForbiddenError(BaseException):
    """Forbidden Error- 403 Status code"""

class ResourceNotFoundError(BaseException):
    """Resource Not found - 404 Status code"""

class ConflictError(BaseException):
    """Conflict Error - 409 Status code"""

class ValidationError(BaseException):
    """Validation Error - 422 Status code"""

class ServiceUnavailableError(BaseException):
    """Service Unavailable - 503 Status code"""

class RequestLibraryError(BaseException):
    """Request Library Error"""

    def __init__(self, *args,**kwargs):
        kwargs['response'] = {}
        kwargs['code'] = -1
        super().__init__(*args,**kwargs)

ERROR_CODE_MAPPING = {
    codes.unauthorized : UnauthorizedError,
    codes.forbidden : ForbiddenError,
    codes.not_found : ResourceNotFoundError,
    codes.conflict : ConflictError,
    codes.unprocessable_entity : ValidationError,
    codes.service_unavailable : ServiceUnavailableError
}

def error_handler(code,response):
    err = ERROR_CODE_MAPPING[code]
    raise err(response=response.json(),code=code)

# warnings
class BaseWarning():
    
    def __init__(self, *args,**kwargs):
        self.logger = Logger.get_logger()
        self.warning_error = True
        process_exception(self)
        super().__init__(*args)
class RequestLibraryWarning(BaseWarning):
    """Request Library Warning"""