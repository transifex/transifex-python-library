# -*- coding: utf-8 -*-
"""
Tests for requests.
"""
import json
import responses
import pytest

from txlib.http.base import BaseRequest
from txlib.http.http_requests import HttpRequest
from txlib.http.auth import AnonymousAuth, BasicAuth
from txlib.http.exceptions import UnknownError, RemoteServerError, \
        AuthorizationError, ConflictError, NotFoundError, RequestError


class TestBaseRequest():
    """Tests for the BaseRequest class."""

    def test_construct_full_hostname(self):
        """Test _construct_full_hostname method."""
        # Test http
        host = "http://www.example.com"
        b = BaseRequest(host)
        assert host == b._hostname

        # Test https
        host = "https://www.example.com"
        b = BaseRequest(host)
        assert host == b._hostname

        # Test unsupported protocols
        for proto in 'ssh', 'ftp':
            with pytest.raises(ValueError):
                BaseRequest(proto + "://www.example.com")

        # Test default protocol
        host = "www.example.com"
        b = BaseRequest(host)
        assert 'https://' + host == b._hostname

    def test_construct_full_url(self):
        """Test _construct_full_url method."""
        # normal case
        host = "http://www.example.com"
        path = "/path/to/resource/"
        b = BaseRequest(host)
        url = b._construct_full_url(path)
        assert host in url
        assert path in url
        assert len(url) == len(host) + len(path)

        # path is missing first '/'
        path = 'path/to/resource'
        url = b._construct_full_url(path)
        assert host in url
        assert path in url
        assert '/' + path in url
        assert len(url) == len(host) + len('/') + len(path)

        # host is missing http part
        host = "www.example.com"
        b = BaseRequest(host)
        url = b._construct_full_url(path)
        assert host in url
        assert path in url
        assert len(url) == (
            len(b.default_scheme) + len('://') + len(host) + len('/')
            + len(path)
        )

        # port is set
        host = "http://www.example.com:8000"
        path = "/path/to/resource/"
        b = BaseRequest(host)
        url = b._construct_full_url(path)
        assert host in url
        assert path in url
        assert len(url) == len(host) + len(path)

        # both hast and path have bakslashes
        host = "http://www.example.com/"
        path = "/path/to/resource/"
        b = BaseRequest(host)
        url = b._construct_full_url(path)
        assert host in url
        assert path in url
        assert len(url) == len(host) - len('/') + len(path)

    def test_error_messages(self):
        """Test the error messages of the requests."""
        b = BaseRequest('www.example.com')
        for code in b.error_messages:
            msg = b.error_messages[code]
            assert msg in b._error_message(code, msg)

    def test_http_exceptions(self):
        """Test the exceptions raised for each HTTP 4xx code."""
        b = BaseRequest('www.example.com')
        for code in b.errors:
            klass = b.errors[code]
            assert b._exception_for(code) is klass
            assert b._exception_for(499) is UnknownError
        for code in (500, 501, 502, ):
            assert b._exception_for(code) is RemoteServerError


class TestHttpRequest():
    """Test the HttpRequest class.

    These tests run against a local transifex installation. We assume
    transifex listens in 127.0.0.1:8000 and there is a user `txlib` that has
    the password `txlib`.
    """

    @pytest.fixture(autouse=True)
    def auto_init(self):
        self.hostname = 'http://127.0.0.1:8000'
        self.username = 'txlib'
        self.password = 'txlib'
        self.headers = {'header-1': 'value-1', 'header-2': 'value-2'}
        self.auth = BasicAuth(self.username, self.password)
        self.auth_with_headers = BasicAuth(self.username, self.password, self.headers)

    @responses.activate
    def test_anonymous_requests(self):
        """Test anonymous requests.

        They should all fail, since transifex currently does not allow
        anonymous access to the API.
        """
        responses.add(responses.GET,
                      "{}/api/2/projects/".format(self.hostname),
                      status=401)
        auth = AnonymousAuth()
        h = HttpRequest(self.hostname, auth=auth)
        with pytest.raises(AuthorizationError):
            h.get('/api/2/projects/')

    @responses.activate
    def test_wrong_auth(self):
        """Test response for requests with wrong authentication info."""
        responses.add(responses.GET,
                      "{}/api/2/projects/".format(self.hostname),
                      status=401)
        auth = BasicAuth(self.username, 'wrong')
        h = HttpRequest(self.hostname, auth=auth)
        with pytest.raises(AuthorizationError):
            h.get('/api/2/projects/')

    @responses.activate
    def test_auth(self):
        """Test authenticated requests."""
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                          "{}/api/2/projects/".format(self.hostname),
                          body='{}', content_type="application/json")
            path = '/api/2/projects/'
            req = HttpRequest(self.hostname, auth=self.auth)
            req.get(path)       # Succeeds!
            # Assert that custom headers do not exist in the request
            for header, value in self.headers.items():
                with pytest.raises(KeyError):
                    assert rsps.calls[0][0].headers[header] == value

    @responses.activate
    def test_auth_with_headers(self):
        """Test authenticated requests with custom headers."""
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                          "{}/api/2/projects/".format(self.hostname),
                          body='{}', content_type="application/json")
            path = '/api/2/projects/'
            req = HttpRequest(self.hostname, auth=self.auth_with_headers)
            req.get(path)
            # Assert that cusotm headers have been added to the request
            for header, value in self.headers.items():
                assert rsps.calls[0][0].headers[header] == value

    @responses.activate
    def test_not_found(self):
        h = HttpRequest(self.hostname, auth=self.auth)
        responses.add(responses.GET,
                      "{}/api/2/txlib/".format(self.hostname),
                      status=404)

        # get a project that does not exist
        with pytest.raises(NotFoundError):
            h.get('/api/2/txlib/')

    def test_create(self):
        with responses.RequestsMock() as rsps:
            h = HttpRequest(self.hostname, auth=self.auth)
            # create a project
            path = '/api/2/projects/'
            rsps.add(responses.POST,
                     "{}/api/2/projects/".format(self.hostname),
                     status=201)
            rsps.add(responses.POST,
                     "{}/api/2/projects/".format(self.hostname),
                     status=409)
            data = json.dumps(dict(slug='txlib', name='Txlib project'))
            h.post(path, data=data)
            with pytest.raises(ConflictError):
                h.post(path, data=data)

    def test_update(self):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.PUT,
                     "{}/api/2/project/txlib/".format(self.hostname),
                     status=400)
            rsps.add(responses.GET,
                     "{}/api/2/project/txlib/?details".format(self.hostname),
                     json={"anyone_submit": False}, match_querystring=True,
                     status=200)
            rsps.add(responses.PUT,
                     "{}/api/2/project/txlib/".format(self.hostname),
                     json={"anyone_submit": True},
                     status=200)
            rsps.add(responses.GET,
                     "{}/api/2/project/txlib/?details".format(self.hostname),
                     json={"anyone_submit": True}, match_querystring=True,
                     status=200)
            rsps.add(responses.DELETE,
                     "{}/api/2/project/txlib/".format(self.hostname),
                     status=200)
            h = HttpRequest(self.hostname, auth=self.auth)
            # Using a non-existent attribute for projects
            data = json.dumps(dict(name='New name', anyone_submitt=True))
            path = '/api/2/project/txlib/'
            with pytest.raises(RequestError):
                h.put(path, data)

            # make sure the field has the default value
            p = h.get(path + '?details')
            assert p['anyone_submit'] is False

            # update the details of the project
            data = json.dumps(dict(name='New name',  anyone_submit=True))
            h.put(path, data)

            # make sure the change has been saved
            p = h.get(path + '?details')
            assert p['anyone_submit'] is True

            # delete the project
            h.delete(path)
