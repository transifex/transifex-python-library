# -*- coding: utf-8 -*-

from txlib.http.auth import AuthInfo, BasicAuth, AnonymousAuth
from txlib.utils.imports import unittest


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
        self.assertIn('headers', updated_req_args)
        self.assertIn('Authorization', updated_req_args['headers'])
        auth_header = updated_req_args['headers']['Authorization']
        req_args = updated_req_args
        updated_req_args = auth_info.populate_request_data(req_args)
        self.assertEqual(
            auth_header, updated_req_args['headers']['Authorization']
        )
        req_args = updated_req_args
        req_args['headers'] = {'User-Agent': 'test'}
        updated_req_args = auth_info.populate_request_data(req_args)
        headers = updated_req_args['headers']
        self.assertIn('User-Agent', headers)
        self.assertIn('Authorization', headers)
        self.assertEqual(len(headers.keys()), 2)

    def test_invalid_auth(self):
        self.assertRaises(ValueError, AuthInfo.get, username='username')
        self.assertRaises(ValueError, AuthInfo.get, password='password')


