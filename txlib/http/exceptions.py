# -*- coding: utf-8 -*-
"""
HTTP related exceptions.
"""


class ServerError(Exception):
    """Base class for exceptions for problems with the remote server."""

    def __init__(self, *args, **kwargs):
        if 'http_code' in kwargs:
            self.http_code = kwargs.pop('http_code')
        super(ServerError, self).__init__(*args, **kwargs)


class RequestError(ServerError):
    """Class to indicate a generic error with the request
    to the remote server.

    This is a 400 error.
    """


class NotFoundError(ServerError):
    """Class to indicate a resource has not been found in the remote server.

    This is for 404 errors"""


class AuthenticationError(ServerError):
    """Class to indicate a problem with the username and/or password.

    This is a 403 error.
    """


class AuthorizationError(ServerError):
    """Class to indicate that authorization is required.

    This is a 401 error.
    """


class ConflictError(ServerError):
    """Class to indicate a conflict for the resource in the server.

    This is a 409 error.
    """


class UnknownError(ServerError):
    """Class for errors which are not handled specifically."""


class RemoteServerError(ServerError):
    """Class for 5xx errors."""


class NoResponseError(ServerError):
    """Exception raised when there was no connection to the remopte server."""
