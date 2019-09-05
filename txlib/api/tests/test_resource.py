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
    def test_get_stats(self, mock_request):
        mock_request.return_value = get_mock_response(
            200, '{"id": 100, "slug": "resource1"}'
        )
        resource = Resource.get(project_slug='project1', slug='resource1')

        mock_request.return_value = get_mock_response(
            200, '{"el": {"completed": "91%"}}'
        )
        stats = resource.get_stats()
        assert stats == {"el": {"completed": "91%"}}

    @patch('txlib.http.http_requests.requests.request')
    def test_save_content(self, mock_request):
        some_content = 'string1\\nstring2\\nstring3'
        mock_request.return_value = get_mock_response(
            200, '{{"content": "{}"}}'
        )
        resource = Resource(project_slug='project1', slug='resource1')
        resource.save(
            name='Resource1',
            content=some_content
        )
        assert resource.slug == 'resource1'
        assert resource.content == some_content

    @patch('txlib.api.resources.Resource._update')
    @patch('txlib.api.resources.Resource._create')
    @patch('txlib.http.http_requests.requests.request')
    def test_create_and_update(self, mock_request, mock_create, mock_update):
        # save a new resource
        resource = Resource(project_slug='project1', slug='resource2')
        resource.save(
            name='Resource2',
            content='string1\\nstring2\\nstring3',
        )
        mock_create.assert_called_once_with(
            content='string1\\nstring2\\nstring3',
            name='Resource2'
        )

        # update an existing resource
        mock_request.return_value = get_mock_response(
            200,
            """{"id": 2, "slug": "resource2", "content": "string1\\nstring2\\nstring3\\nstring4"}"""
        )
        resource = Resource.get(project_slug='project2', slug='resource2')
        resource.save(
            name='Resource2',
            content='string1\\nstring2\\nstring3\\nstring4',
        )
        mock_update.assert_called_once_with(
            content='string1\\nstring2\\nstring3\\nstring4',
            name='Resource2'
        )

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

    @patch('txlib.http.http_requests.HttpRequest.post')
    def test_binary_file_create(self, mock_post):
        """Test that a binary file creation calls post method."""
        resource = Resource(project_slug='project1', slug='resource2')
        resource.save(
            name='Resource2',
            content=b'string1\\nstring2\\nstring3',
            i18n_type='XLSX'
        )
        assert mock_post.called

    @patch('txlib.http.http_requests.requests.request')
    @patch('txlib.http.http_requests.HttpRequest.put')
    def test_binary_file_update(self, mock_put, mock_request):
        """Test that a binary file update calls put method."""
        mock_request.return_value = get_mock_response(
            200,
            """{"id": 2, "slug": "resource2", "content": "string1\\nstring2\\nstring3\\nstring4"}"""
        )
        resource = Resource.get(project_slug='project2', slug='resource2')
        resource.save(
            name='Resource2',
            content=b'string1\\nstring2\\nstring3\\nstring4',
            i18n_type='XLSX'
        )
        assert mock_put.called
