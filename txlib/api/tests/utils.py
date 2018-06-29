import pytest

from txlib.http.http_requests import HttpRequest
from txlib.registry import registry


class TestResponse():
    """A convenient class that represents an HTTP response, with only
    a few fields, which are necessary for testing."""

    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content

    @property
    def ok(self):
        return self.status_code < 400


def setup_registry():
    """Initializes the registry and sets up an `http_handler`."""
    conn = HttpRequest('http://doesntmatter.org')
    registry.setup({'http_handler': conn})


def get_mock_response(status_code, content):
    """Return a test response with the given parameters.

    If the registry hasn't been set up yet, it sets it up
    and adds an http_handler entry.

    :param int status_code: the HTTP status code of the response
    :param str content: the content of the response
    :return: the response object for testing
    :rtype: TestResponse
    """
    if not registry.http_handler:
        setup_registry()

    return TestResponse(status_code, content.encode('utf-8'))


@pytest.fixture
def clean_registry():
    """Run the test and the remove the `http_handler` entry from
    the registry."""
    yield
    registry.remove('http_handler')

