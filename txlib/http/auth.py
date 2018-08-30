# -*- coding: utf-8 -*-
"""
Authentication related module.
"""
from __future__ import unicode_literals

from requests.auth import HTTPBasicAuth


class AuthInfo(object):
    """Base class for all AuthInfo classes."""

    @classmethod
    def get(self, username=None, password=None, headers={}):
        """Factory method to get the correct AuthInfo object.

        The returned value depends on the arguments given. In case the
        username and password don't have a value (ie evaluate to False),
        return an object for anonymous access. Else, return an auth
        object that supports basic authentication.

        Args:
            `username`: The username of the user.
            `password`: The password of the user.
            `headers`: Custom headers to be sent to each request.
        Raises:
            ValueError in case one of the two arguments evaluates to False,
            (such as having the None value).
        """
        if all((username, password, )):
            return BasicAuth(username, password, headers)
        elif not any((username, password, )):
            return AnonymousAuth(headers)
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

    def __init__(self, username, password, headers={}):
        """Initializer.

        :param str username: The username to be used for the authentication with
            Transifex. It can either have the value 'API' (suggested) or the
            username of a user
        :param str password: The password to be used for the authentication with
            Transifex. It should be a Transifex token (suggested) if the username is
            'API', or the password of the user whose username is used for authentication
        :param dict headers: A dictionary with custom headers which will be sent
            in every request to the Transifex API.
        """
        self._username = username
        self._password = password
        self._headers = headers

    def populate_request_data(self, request_args):
        """Add the authentication info to the supplied dictionary.

        We use the `requests.HTTPBasicAuth` class as the `auth` param.

        Args:
            `request_args`: The arguments that will be passed to the request.
        Returns:
            The updated arguments for the request.
        """
        request_args['auth'] = HTTPBasicAuth(
            self._username, self._password)
        return request_args


class AnonymousAuth(AuthInfo):
    """Class for anonymous access."""

    def __init__(self, headers={}):
        """Initializer.

        :param dict headers: A dictionary with custom headers which will be sent
            in every request to the Transifex API.
        """
        self._headers = headers
