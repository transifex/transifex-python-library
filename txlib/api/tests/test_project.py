# -*- coding: utf-8 -*-
import pytest

from txlib.api.project import Project
from txlib.api.tests.utils import clean_registry, get_mock_response
from txlib.tests.compat import patch


@pytest.fixture(autouse=True)
def auto_clean_registry():
    """Run the test and the remove the `http_handler` entry from
    the registry."""
    clean_registry()


class TestProjectModel():
    """Test the functionality of the Project model."""

    @patch('txlib.http.http_requests.requests.request')
    def test_get_populates_object(self, mock_request):
        mock_request.return_value = get_mock_response(
            200, '{"id": 100, "slug": "project1"}'
        )
        obj = Project.get(slug='project1')

        assert obj.id == 100
        assert obj.slug == 'project1'
        assert '{}'.format(obj) == '[Project slug=project1]'
