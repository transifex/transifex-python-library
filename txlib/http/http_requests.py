# -*- coding: utf-8 -*-

import json
import requests
from io import BytesIO
from txlib.utils import _logger
from txlib.http.base import BaseRequest
from txlib.http.exceptions import NoResponseError


class HttpRequest(BaseRequest):
    """Basic http requests handler.

    This class can handle both HTTP and HTTPS requests.
    """

    def get(self, path, params=None):
        """Make a GET request.

        Args:
            `path`: The path to the resource.
        Returns:
            The content of the response.
        Raises:
            An exception depending on the HTTP status code of the response.
        """
        return json.loads(self._make_request('GET', path, params=params))

    def post(self, path, data, content=None):
        """Make a POST request.

        If a `filename` is not specified, then the data must already be
        JSON-encoded. We specify the Content-Type accordingly.

        Else, we make a multipart/form-encoded request. In this case, the data
        variable must be a dict-like object. The file must already be
        suitably (usually UTF-8) encoded.

        Args:
            `path`: The path to the resource.
            `data`: The data to send. The data must already be JSON-encoded.
            `content`: The bytes (binary form) of the content to send.
        Returns:
            The content of the response.
        Raises:
            An exception depending on the HTTP status code of the response.
        """
        return self._send('POST', path, data, content)

    def put(self, path, data, content=None):
        """Make a PUT request.

        If a `filename` is not specified, then the data must already be
        JSON-encoded. We specify the Content-Type accordingly.

        Else, we make a multipart/form-encoded request. In this case, the data
        variable must be a dict-like object. The file must already be
        suitably (usually UTF-8) encoded.

        Args:
            `path`: The path to the resource.
            `data`: The data to send. The data must already be JSON-encoded.
            `content`: The bytes (binary form) of the content to send.
        Returns:
            The content of the response.
        Raises:
            An exception depending on the HTTP status code of the response.
        """
        return self._send('PUT', path, data, content)

    def delete(self, path):
        """Make a DELETE request.

        Args:
            `path`: The path to the resource.
        Returns:
            The content of the response.
        Raises:
            An exception depending on the HTTP status code of the response.
        """
        return self._make_request('DELETE', path)

    def _make_request(self, method, path, data=None, params=None, **kwargs):
        """Make a request.

        Use the `requests` module to actually perform the request.

        Args:
            `method`: The method to use.
            `path`: The path to the resource.
            `data`: Any data to send (for POST and PUT requests).
            `kwargs`: Other parameters for `requests`.
        Returns:
            The content of the response.
        Raises:
            An exception depending on the HTTP status code of the response.
        """
        _logger.debug("Method for request is %s" % method)
        url = self._construct_full_url(path)
        _logger.debug("URL for request is %s" % url)
        self._auth_info.populate_request_data(kwargs)
        _logger.debug("The arguments are %s" % kwargs)

        # Add custom headers for the request
        if self._auth_info._headers:
            kwargs.setdefault('headers', {}).update(self._auth_info._headers)

        res = requests.request(method, url, data=data, params=params, **kwargs)

        if res.ok:
            _logger.debug("Request was successful.")
            return res.content.decode('utf-8')

        if hasattr(res, 'content'):
            _logger.debug("Response was %s:%s", res.status_code, res.content)
            raise self._exception_for(res.status_code)(
                res.content, http_code=res.status_code
            )
        else:
            msg = "No response from URL: %s" % res.request.url
            _logger.error(msg)
            raise NoResponseError(msg)

    def _send(self, method, path, data, content):
        """Send data to a remote server, either with a POST or a PUT request.

        Args:
            `method`: The method (POST or PUT) to use.
            `path`: The path to the resource.
            `data`: The data to send.
            `content`: The bytes (binary form) of the content to send.
        Returns:
            The content of the response.
        Raises:
            An exception depending on the HTTP status code of the response.
        """
        if content is None:
            return self._send_json(method, path, data)
        else:
            return self._send_file(method, path, data, content)

    def _send_json(self, method, path, data):
        """Make a application/json request.

        Args:
            `method`: The method of the request (POST or PUT).
            `path`: The path to the resource.
            `data`: The JSON-encoded data.
        Returns:
            The content of the response.
        Raises:
            An exception depending on the HTTP status code of the response.
        """
        headers = {'Content-type': 'application/json'}
        return self._make_request(method, path, data=data, headers=headers)

    def _send_file(self, method, path, data, content):
        """Make a multipart/form-encoded request.

        The content to send is opened in binary mode to report correct byte length.

        Args:
            `method`: The method of the request (POST or PUT).
            `path`: The path to the resource.
            `data`: The JSON-encoded data.
            `content`: The bytes (binary form) of the content to send.
        Returns:
            The content of the response.
        Raises:
            An exception depending on the HTTP status code of the response.
        """
        return self._make_request(method, path, data=data, files={"file": BytesIO(content)})

