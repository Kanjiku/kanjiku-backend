
from sanic.exceptions import SanicException

class RegistrationFail(SanicException):
    pass

class UserDoesNotExist(SanicException):
    pass

class LoginError(SanicException):
    pass