# -*- coding: utf-8 -*-
import pytest

from txlib.api.resources import Resource
from txlib.tests.compat import patch
from txlib.api.tests.utils import clean_registry, get_mock_response


@pytest.fixture(scope='module', autouse=True)
def auto_clean_registry():
    """Run the test and the remove the `http_handler` entry from
    the registry."""
    yield
    clean_registry()


class TestResourceModel():
    """Test the functionality of the Resource model."""

    @patch('txlib.http.http_requests.requests.request')
    def test_get_populates_object(self, mock_request):
        mock_request.return_value = get_mock_response(
            200, '{"id": 100, "slug": "resource1"}'
        )
        obj = Resource.get(project_slug='project1', slug='resource1')

        assert obj.id == 100
        assert obj.slug == 'resource1'
        assert '{}'.format(obj) == '[Resource slug=resource1]'

    @patch('txlib.http.http_requests.requests.request')
    def test_retrieve_content(self, mock_request):
        mock_request.return_value = get_mock_response(
            200, '{"id": 100, "slug": "resource1"}'
        )
        resource = Resource.get(project_slug='project1', slug='resource1')

        mock_request.return_value = get_mock_response(
            200, '{"content": "string1\\nstring2\\nstring3"}'
        )
        content = resource.retrieve_content()
        assert content == 'string1\nstring2\nstring3'

    @patch('txlib.http.http_requests.requests.request')
    def test_save_content(self, mock_request):
        mock_request.return_value = get_mock_response(
            200, '{"content": "string1\\nstring2\\nstring3"}'
        )

        resource = Resource(project_slug='project1', slug='resource1')
        resource.save(
            name='Resource1',
            content='string1\\nstring2\\nstring3'
        )
        assert resource.slug == 'resource1'
        assert resource.content == 'string1\\nstring2\\nstring3'

    @patch('txlib.http.http_requests.requests.request')
    def test_update_content(self, mock_request):
        """Test the update of a Resource when a 'content' parameter is set.

        The `content` parameter needs an additional API request,
        so it is handled separately.
        """
        mock_request.return_value = get_mock_response(
            200, '{"id": 100, "slug": "resource1"}'
        )
        resource = Resource.get(project_slug='project1', slug='resource1')

        mock_request.return_value = get_mock_response(
            200, '{"content": "only_one_string"}'
        )
        resource.save(
            name='Resource--1',
            content='only_one_string'
        )
        assert resource.content == 'only_one_string'

    @patch('txlib.http.http_requests.requests.request')
    def test_update(self, mock_request):
        """Test the update of a Resource when no 'content' parameter is set."""
        mock_request.return_value = get_mock_response(
            200, '{"id": 100, "slug": "resource1"}'
        )
        resource = Resource.get(project_slug='project1', slug='resource1')

        mock_request.return_value = get_mock_response(
            200, '{"content": "only_one_string"}'
        )
        resource.save(
            name='Resource--1',
        )
        assert resource.name == 'Resource--1'
