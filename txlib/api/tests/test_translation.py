# -*- coding: utf-8 -*-
import pytest

from txlib.api.translations import Translation
from txlib.tests.compat import patch
from txlib.api.tests.utils import clean_registry, get_mock_response


@pytest.fixture(scope='module', autouse=True)
def auto_clean_registry():
    """Run the test and the remove the `http_handler` entry from
    the registry."""
    yield
    clean_registry()


class TestTranslationModel():
    """Test the functionality of the Translation model."""

    @patch('txlib.http.http_requests.requests.request')
    def test_get_translation(self, mock_request):
        mock_request.return_value = get_mock_response(
            200, u'{"content": {"Master_key": "τεστ"}}'
        )
        obj = Translation.get(project_slug='project1', slug='resource1', lang='el')
        assert obj.lang == 'el'
        assert obj.content == {'Master_key': u'τεστ'}

    @patch('txlib.http.http_requests.requests.request')
    def test_put_translation(self, mock_request):
        mock_request.return_value = get_mock_response(
            200, '{\
                    "strings_added": 1,\
                    "strings_updated": 0,\
                    "strings_delete": 0,\
                    "redirect": ""\
                  }'
        )
        content = 'string1\\nstring2\\nstring3'
        translation = Translation(
            project_slug='project1', slug='resource1', lang='el'
        )
        translation.save(content=content)
        assert translation.lang == 'el'
        assert translation.content == content

    @patch('txlib.http.http_requests.requests.request')
    @patch('txlib.http.http_requests.HttpRequest.put')
    def test_put_translation_binary(self, mock_put, mock_req):
        """Test that a binary translation file calls put method."""
        mock_req.return_value = get_mock_response(
            200, '{\
                            "project_slug": "project1",\
                            "slug": "resource1",\
                            "lang": "en",\
                            "i18n_type": "XLSX"\
                          }'
        )

        translation = Translation(
            project_slug='project1', slug='resource1', lang='el'
        )
        translation.save(content=b'string1\\nstring2\\nstring3\\nstring4')
        assert mock_put.called


