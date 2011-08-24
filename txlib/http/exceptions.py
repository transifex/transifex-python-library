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
    """
    pass


class NotFoundError(ServerError):
    """Class to indicate a resource has not been found in the remote server."""
    pass


class AuthenticationError(ServerError):
    """Class to indicate a problem with the username and/or password."""
    pass


class AuthorizationError(ServerError):
    """Class to indicate that authorization is required."""
    pass


class UnknownError(ServerError):
    """Class for errors which are not handled specifically."""
    pass


class RemoteServerError(ServerError):
    """Class for 5xx errors."""
