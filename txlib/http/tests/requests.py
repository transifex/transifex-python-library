# -*- coding: utf-8 -*-
"""
Tests for requests.
"""

from txlib.utils import json
from txlib.utils.imports import unittest
from txlib.http.base import BaseRequest
from txlib.http.http_requests import HttpRequest
from txlib.http.auth import AnonymousAuth, BasicAuth
from txlib.http.exceptions import UnknownError, RemoteServerError, \
        AuthorizationError, ConflictError, NotFoundError, RequestError


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


class TestHttpRequest(unittest.TestCase):
    """Test the HttpRequest class.

    These tests run against a local transifex installation. We assume
    transifex listens in 127.0.0.1:8000 and there is a user `txlib` that has
    the password `txlib`.
    """

    @classmethod
    def setUpClass(cls):
        cls.hostname = 'http://127.0.0.1:8000'
        cls.username = 'txlib'
        cls.password = 'txlib'
        cls.auth = BasicAuth(cls.username, cls.password)

    def test_anonymous_requests(self):
        """Test anonymous requests.

        They should all fail, since transifex currently does not allow
        anonymous access to the API.
        """
        auth = AnonymousAuth()
        h = HttpRequest(self.hostname, auth=auth)
        self.assertRaises(AuthorizationError, h.get, '/api/2/projects/')

    def test_wrong_auth(self):
        """Test response for requests with wrong authentication info."""
        auth = BasicAuth(self.username, 'wrong')
        h = HttpRequest(self.hostname, auth=auth)
        self.assertRaises(AuthorizationError, h.get, '/api/2/projects/')

    def test_auth(self):
        """Test authenticated requests."""
        path = '/api/2/projects/'
        h = HttpRequest(self.hostname, auth=self.auth)
        res = h.get(path)       # Succeeds!

    def test_script(self):
        h = HttpRequest(self.hostname, auth=self.auth)

        # get a project that does not exist
        self.assertRaises(NotFoundError, h.get, '/api/2/txlib/')

        # create a project
        data = json.dumps(dict(slug='txlib', name='Txlib project'))
        path = '/api/2/projects/'
        h.post(path, data=data)

        # creating the same project results in an error raised.
        self.assertRaises(ConflictError, h.post, path, data=data)

        # Using a non-existent attribute for projects
        data = json.dumps(dict(name='New name', anyone_submitt=True))
        path = '/api/2/project/txlib/'
        self.assertRaises(RequestError, h.put, path, data)

        # make sure the field has the default value
        p = h.get(path + '?details')
        self.assertFalse(p['anyone_submit'])

        # update the details of the project
        data = json.dumps(dict(name='New name',  anyone_submit=True))
        h.put(path, data)

        # make sure the change has been saved
        p = h.get(path + '?details')
        self.assertTrue(p['anyone_submit'])

        # delete the project
        h.delete(path)
