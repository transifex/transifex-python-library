# -*- coding: utf-8 -*-
import pytest

from txlib.http.auth import AuthInfo, BasicAuth, AnonymousAuth


class TestAuthInfo():
    """Tests for the AuthInfo class."""

    def test_anonymous(self):
        """Test the anonymous user."""
        username, password = None, None
        auth_info = AuthInfo.get(username, password)
        assert isinstance(auth_info, AnonymousAuth)
        req_args = {'foo': 'bar', }
        updated_req_args = auth_info.populate_request_data(req_args)
        assert req_args == updated_req_args
        assert auth_info._headers == {}

    def test_anonymous_with_headers(self):
        """Test the anonymous user with custom headers."""
        username, password = None, None
        headers = {'test-header-1': 'test-value-1', 'test-header-2': 'test-value-2'}
        auth_info = AuthInfo.get(username=username, password=password, headers=headers)
        assert isinstance(auth_info, AnonymousAuth)
        assert auth_info._headers == headers

    def test_authenticated(self):
        username, password = 'username', 'password'
        auth_info = AuthInfo.get(username=username, password=password)
        assert isinstance(auth_info, BasicAuth)
        req_args = {'foo': 'bar'}
        updated_req_args = auth_info.populate_request_data(req_args)
        assert 'foo' in updated_req_args
        assert 'auth' in updated_req_args
        assert auth_info._headers == {}

    def test_authenticated_with_headers(self):
        username, password = 'username', 'password'
        headers = {'test-header-1': 'test-value-1', 'test-header-2': 'test-value-2'}
        auth_info = AuthInfo.get(username=username, password=password, headers=headers)
        assert isinstance(auth_info, BasicAuth)
        assert auth_info._headers == headers
        
    def test_invalid_auth(self):
        with pytest.raises(ValueError):
            AuthInfo.get(username='username')

        with pytest.raises(ValueError):
            AuthInfo.get(password='password')
