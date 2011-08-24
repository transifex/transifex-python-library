# -*- coding: utf-8 -*-
"""
Tests for requests.
"""

from txlib.http.base import BaseRequest
from txlib.http.exceptions import UnknownError, RemoteServerError
from txlib.http.tests import unittest


class TestBaseRequest(unittest.TestCase):
    """Tests for the BaseRequest class."""

    def test_construct_full_hostname(self):
        """Test _construct_full_hostname method."""
        # Test http
        host = "http://www.example.com"
        b = BaseRequest(host)
        self.assertEquals(host, b._hostname)

        # Test https
        host = "https://www.example.com"
        b = BaseRequest(host)
        self.assertEquals(host, b._hostname)

        # Test unsupported protocols
        for proto in 'ssh', 'ftp':
            self.assertRaises(
                ValueError, BaseRequest, proto + "://www.example.com"
            )

        # Test default protocol
        host = "www.example.com"
        b = BaseRequest(host)
        self.assertEquals('https://' + host, b._hostname)


    def test_construct_full_url(self):
        """Test _construct_full_url method."""
        # normal case
        host = "http://www.example.com"
        path = "/path/to/resource/"
        b = BaseRequest(host)
        url = b._construct_full_url(path)
        self.assertIn(host, url)
        self.assertIn(path, url)
        self.assertEquals(len(url), len(host) + len(path))

        # path is missing first '/'
        path = 'path/to/resource'
        url = b._construct_full_url(path)
        self.assertIn(host, url)
        self.assertIn(path, url)
        self.assertIn('/' + path, url)
        self.assertEquals(len(url), len(host) + len('/') + len(path))

        # host is missing http part
        host = "www.example.com"
        b = BaseRequest(host)
        url = b._construct_full_url(path)
        self.assertIn(host, url)
        self.assertIn(path, url)
        self.assertEquals(
            len(url),
            len(b.default_scheme) + len('://') + len(host) + len('/') +\
                len(path)
        )

        # port is set
        host = "http://www.example.com:8000"
        path = "/path/to/resource/"
        b = BaseRequest(host)
        url = b._construct_full_url(path)
        self.assertIn(host, url)
        self.assertIn(path, url)
        self.assertEquals(len(url), len(host) + len(path))

        # both hast and path have bakslashes
        host = "http://www.example.com/"
        path = "/path/to/resource/"
        b = BaseRequest(host)
        url = b._construct_full_url(path)
        self.assertIn(host, url)
        self.assertIn(path, url)
        self.assertEquals(len(url), len(host) - len('/') + len(path))

    def test_error_messages(self):
        """Test the error messages of the requests."""
        b = BaseRequest('www.example.com')
        for code, msg in b.error_messages.iteritems():
            self.assertIn(msg, b._error_message(code, msg))

    def test_http_exceptions(self):
        """Test the exceptions raised for each HTTP 4xx code."""
        b = BaseRequest('www.example.com')
        for code, klass in b.errors.iteritems():
            self.assertIs(b._exception_for(code), klass)
        self.assertIs(b._exception_for(499), UnknownError)
        for code in (500, 501, 502, ):
            self.assertIs(b._exception_for(code), RemoteServerError)
