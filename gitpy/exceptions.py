import traceback
from gitpy.service.loggerService import Logger
from requests.status_codes import codes

class BaseException(IOError):
    
    def __init__(self, *args,**kwargs):
        self.msg = args[0]
        self.response = kwargs.pop('response')
        self.code = kwargs.pop('code')
        self.logger = Logger.get_logger()
        tb = traceback.extract_stack()[:-1]  # Exclude current frame        
        if tb:
            last_frame = None
            if(hasattr(self,"warning_error")):
                last_frame = tb[-4] # added one more stack frame
            else:
                last_frame = tb[-3]
            file_name = last_frame.filename
            line_no = last_frame.lineno
            func_name = last_frame.name
            if(hasattr(self,"warning_error")):
                self.logger.warning(f'{file_name} , {func_name}(), {line_no} , {self.__repr__()} ----- err_msg :  {self.msg} - actual_response : {self.response}')
            else:
                self.logger.error(f'{file_name} , {func_name}(), {line_no} , {self.__repr__()} ----- err_msg :  {self.msg} - actual_response : {self.response}')
        else:
            self.logger.error(f'err_msg :  {self.msg} - actual_response : {self.response}')
        super().__init__(*args)

class UnauthorizedError(BaseException):
    """Resource Not found - 401 Status code"""

class ForbiddenError(BaseException):
    """Resource Not found - 403 Status code"""

class ResourceNotFoundError(BaseException):
    """Resource Not found - 404 Status code"""

class RequestLibraryError(BaseException):
    """Request Library Error"""

class RequestLibraryWarning(BaseException):
    """Request Library Warning"""

    def __init__(self, *args, **kwargs):
        self.warning_error = True
        super().__init__(*args, **kwargs)

# new error message for every status_code returned by API unique and different
class ERR_MSG:
    USER_NOT_FOUND = 'User not found'
    FORBIDDEN_USER = 'Forbidden User'
    UNAUTHORIZED = "Unauthorized, token not valid"
    REQUEST_LIBRARY_ERROR = "warnings from request library"
    REQUEST_LIBRARY_WARNING = "error from request library"

# extend for every function defined
class FUNCTIONS:
    AUTHENICATION = "AUTHENICATION"

# mapping for every function defined
ERROR_MSG_MAPPING = {
    FUNCTIONS.AUTHENICATION : {
        codes.unauthorized : ERR_MSG.USER_NOT_FOUND,
        codes.forbidden : ERR_MSG.FORBIDDEN_USER,
        codes.not_found : ERR_MSG.USER_NOT_FOUND
    }
}

# one time mapping for every status code
# generic errors will be defined and thrown but the message related to API will be mapped based on status code
ERROR_CODE_MAPPING = {
    codes.unauthorized : UnauthorizedError,
    codes.forbideen : ForbiddenError,
    codes.not_found : ResourceNotFoundError
}

def error_handler(code,fxns,response):
    # get the message
    # raise ResourceNotFoundError(ERR_MSG.USER_NOT_FOUND,response=response.json(),code=code)
    err_msg = ERROR_MSG_MAPPING[fxns][code]
    err = ERROR_CODE_MAPPING[code]
    raise err(err_msg,response=response.json(),code=code)