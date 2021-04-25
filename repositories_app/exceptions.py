"""
Module with custom exceptions that might raise during
application runtime.
"""


class UserNotFoundServiceException(Exception):
    """
    Exception raised in a service, when call to a service
    was not successful, because desired user was not found.
    """

    def __init__(self):
        message = "Desired user not found."
        super().__init__(message)


class ApiRateLimitExceededServiceException(Exception):
    """
    Exception raised in a service, when call to a service
    was not successful due to exceeded limit of calls to api.
    """

    def __init__(self):
        message = "Api rate limit exceeded."
        super().__init__(message)


class BadCredentialsServiceException(Exception):
    """
    Exception raised in a service, when call to a service
    was not successful due to incorrect credentials.
    """

    def __init__(self):
        message = "Bad credentials were provided."
        super().__init__(message)


class UnprocessableEntityServiceException(Exception):
    """
    Exception raised in a service, when call to a service
    returned code 422: Unprocessable Entity.
    """

    def __init__(self, message):
        super().__init__(message)
