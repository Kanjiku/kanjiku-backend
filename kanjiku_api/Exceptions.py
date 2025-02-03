from sanic.exceptions import SanicException


class ParameterError(SanicException):
    pass


class RegistrationFail(SanicException):
    pass


class UserDoesNotExist(SanicException):
    pass


class LoginError(SanicException):
    pass


class SessionError(SanicException):
    pass

class PermissionError(SanicException):
    pass