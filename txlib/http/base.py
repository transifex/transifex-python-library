# -*- coding: utf-8 -*-

from __future__ import with_statement
import urlparse
from txlib.http.auth import AnonymousAuth
from txlib.http.exceptions import *
from txlib.utils import _logger


class BaseRequest(object):
    """Base class for http request classes."""

    errors = {
        400: RequestError,
        401: AuthorizationError,
        403: AuthenticationError,
        404: NotFoundError,
        409: ConflictError,
    }

    success = {
        200: "OK",
        201: "Created",
        204: "Deleted",
    }

    error_messages = {
        400: "Bad request: %s",
        401: "Authorization is required: %s",
        403: "Authentication error: %s",
        404: "Entity was not found: %s",
        409: "Error with the request: %s",
    }

    default_scheme = 'https'

    def __init__(self, hostname, auth=AnonymousAuth()):
        """Initializer for the base class.

        Save the hostname to use for all requests as well as any
        authentication info needed.

        Args:
            hostname: The host for the requests.
            auth: The authentication info needed for any requests.
        """
        self._hostname = self._construct_full_hostname(hostname)
        _logger.debug("Hostname is %s" % self._hostname)
        self._auth_info = auth

    def _construct_full_hostname(self, hostname):
        """Create a full (scheme included) hostname from the argument given.

        Only HTTP and HTTP+SSL protocols are allowed.

        Args:
            hostname: The hostname to use.
        Returns:
            The full hostname.
        Raises:
            ValueError: A not supported protocol is used.
        """
        if hostname.startswith(('http://', 'https://', )):
            return hostname
        if '://' in hostname:
            protocol, host = hostname.split('://', 1)
            raise ValueError('Protocol %s is not supported.' % protocol)
        return '://'.join([self.default_scheme, hostname, ])

    def _construct_full_url(self, path):
        """Construct the full url from the host and the path parts."""
        return urlparse.urljoin(self._hostname, path)

    def _error_message(self, code, msg):
        """Return the message that corresponds to the
        request (status code and error message) specified.

        Args:
            `code`: The http status code.
            `msg`: The message to display.
        Returns:
             The error message for the code given.
        """
        return self.error_messages[code] % msg

    def _exception_for(self, code):
        """Return the exception class suitable for the specified HTTP
        status code.

        Raises:
            UnknownError: The HTTP status code is not one of the knowns.
        """
        if code in self.errors:
            return self.errors[code]
        elif 500 <= code < 599:
            return RemoteServerError
        else:
            return UnknownError
