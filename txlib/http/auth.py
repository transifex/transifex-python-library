# -*- coding: utf-8 -*-
"""
Authentication related module.
"""

import base64


class AuthInfo(object):
    """Base class for all AuthInfo classes."""

    @classmethod
    def get(self, username=None, password=None):
        """Factory method to get the correct AuthInfo object.

        The returned value depends on the arguments given. In case the
        username and password don't have a value (ie evaluate to False),
        return an object for anonymous access. Else, return an auth
        object that supports basic authentication.

        Args:
            `username`: The username of the user.
            `password`: The password of the user.
        Raises:
            ValueError in case one of the two arguments evaluates to False,
            (such as having the None value).
        """
        if all((username, password, )):
            return BasicAuth(username, password)
        elif not any((username, password, )):
            return AnonymousAuth()
        else:
            if username is None:
                data = ("username", username, )
            else:
                data = ("Password", password, )
            msg = "%s must have a value (instead of '%s')" % (data[0], data[1])
            raise ValueError(msg)

    def populate_request_data(self, request_args):
        """Add any auth info to the arguments of the (to be performed) request.

        The method of the base class does nothing.

        Args:
            `request_args`: The arguments of the next request.
        Returns:
            The updated arguments for the request.
        """
        return request_args


class BasicAuth(AuthInfo):
    """Class for basic authentication support."""

    def __init__(self, username, password):
        """Initializer."""
        self._username = username
        self._password = password

    def populate_request_data(self, request_args):
        """Add the authentication info to the supplied dictionary.

        We add the `Authorization` header to the arguments of the request
        (without removing any).

        Args:
            `request_args`: The arguments that will be passed to the request.
        Returns:
            The updated arguments for the request.
        """
        headers = request_args.get('headers', {})
        headers.update(self._create_auth_header())
        request_args['headers'] = headers
        return request_args

    def _create_auth_header(self):
        """Create the header for basic authentication."""
        auth_string = base64.encodestring(
            '%s:%s' % (self._username, self._password)
        ).replace('\n', '')
        auth_value = "Basic %s" % auth_string
        return {'Authorization': auth_value}


class AnonymousAuth(AuthInfo):
    """Class for anonymous access."""
