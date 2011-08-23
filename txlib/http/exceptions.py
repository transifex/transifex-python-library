# -*- coding: utf-8 -*-
"""
HTTP related exceptions.
"""


class RemoteServerError(Exception):
    """Base class for exceptions for problems with the remote server."""

    def __init__(self, *args, **kwargs):
        if 'http_code' in kwargs:
            self.http_code = kwargs.pop('http_code')
        super(RemoteServerError, self).__init__(*args, **kwargs)


class RequestError(RemoteServerError):
    """Class to indicate a generic error with the request
    to the remote server.
    """
    pass


class NotFoundError(RemoteServerError):
    """Class to indicate a resource has not been found in the remote server."""
    pass


class AuthenticationError(RemoteServerError):
    """Class to indicate a problem with the username and/or password."""
    pass


class AuthorizationError(RemoteServerError):
    """Class to indicate that authorization is required."""
    pass


class UnknownError(RemoteServerError):
    """Class for errors which are not handled specifically."""
    pass
