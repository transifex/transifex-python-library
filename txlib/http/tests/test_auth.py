# -*- coding: utf-8 -*-
import unittest

from txlib.http.auth import AuthInfo, BasicAuth, AnonymousAuth


class TestAuthInfo(unittest.TestCase):
    """Tests for the AuthInfo class."""

    def test_anonymous(self):
        """Test the anonymous user."""
        username, password = None, None
        auth_info = AuthInfo.get(username, password)
        self.assertIsInstance(auth_info, AnonymousAuth)
        req_args = {'foo': 'bar', }
        updated_req_args = auth_info.populate_request_data(req_args)
        self.assertEqual(req_args, updated_req_args)

    def test_authenticated(self):
        username, password = 'username', 'password'
        auth_info = AuthInfo.get(username=username, password=password)
        self.assertIsInstance(auth_info, BasicAuth)
        req_args = {'foo': 'bar'}
        updated_req_args = auth_info.populate_request_data(req_args)
        self.assertIn('foo', updated_req_args)
        self.assertIn('auth', updated_req_args)

    def test_invalid_auth(self):
        self.assertRaises(ValueError, AuthInfo.get, username='username')
        self.assertRaises(ValueError, AuthInfo.get, password='password')
