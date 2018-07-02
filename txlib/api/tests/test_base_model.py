# -*- coding: utf-8 -*-
import pytest

from txlib.api.base import BaseModel
from txlib.api.tests.utils import clean_registry, get_mock_response
from txlib.tests.compat import patch


@pytest.fixture(scope='module', autouse=True)
def auto_clean_registry():
    """Run the test and the remove the `http_handler` entry from
    the registry."""
    yield
    clean_registry()


class DummyModel(BaseModel):
    """A dummy class useful for testing behaviour that requires
    some configuration that is not defined in BaseModel."""
    writable_fields = {'name', 'description'}
    url_fields = {'slug'}


class TestBaseModel():
    """Test the base model for the Transifex model wrappers."""

    def test_join_subpaths(self):
        """Test that subpaths are joined correctly."""
        b = BaseModel()
        correct_path = '/api/2/projects/'

        # all subpaths have slashes
        path = b._join_subpaths('/api/', '/2/', '/projects/')
        assert path.count('/') == 4
        assert path == correct_path

        # none subpath has slashes
        path = b._join_subpaths('/api', '2', 'projects/')
        assert path.count('/') == 4
        assert path == correct_path

        # there are some slashes
        path = b._join_subpaths('/api/', '2/', 'projects/')
        assert path.count('/') == 4
        assert path == correct_path

    @patch('txlib.http.http_requests.requests.request')
    def test_get_populates_object(self, mock_request):
        mock_request.return_value = get_mock_response(
            200, '{"id": 100, "slug": "slug"}'
        )

        obj = DummyModel.get(slug='slug')
        assert obj.id == 100
        assert obj.slug == 'slug'
        assert obj._populated_fields == {"id": 100, "slug": "slug"}

    def test_setting_invalid_field_raises_error(self):
        obj = DummyModel(slug='slug')
        obj.name = 'name'
        obj.description = 'description'
        with pytest.raises(AttributeError):
            obj.invalid_field = ''

    @patch('txlib.http.http_requests.requests.request')
    def test_saving_existing_object_updates_it(self, mock_request):
        mock_request.return_value = get_mock_response(
            200, '{"id": 100, "slug": "slug"}'
        )
        obj = DummyModel.get(slug='slug')

        mock_request.return_value = get_mock_response(
            200, '{"id": 100, "slug": "slug", '
                 '"description": "description", "name": "name"}'
        )
        obj.save(
            description='description',
            name='name'
        )

        assert obj.name == 'name'
        assert obj.description == 'description'
        assert mock_request.call_count == 2

    @patch('txlib.http.http_requests.requests.request')
    def test_saving_empty_object_does_not_make_request(self, mock_request):
        mock_request.return_value = get_mock_response(
            200, '{"id": 100, "slug": "slug"}'
        )
        obj = DummyModel.get(slug='slug')
        obj.save()

        # The mock request should only have been called once,
        # for `.get()`. The next call, `.save()` should not result
        # to a request, because no attribute was actually set
        assert mock_request.call_count == 1

    @patch('txlib.http.http_requests.requests.request')
    def test_delete_existing_object(self, mock_request):
        mock_request.return_value = get_mock_response(
            200, '{"id": 100, "slug": "slug"}'
        )
        obj = DummyModel.get(slug='slug')

        mock_request.return_value = get_mock_response(
            200, '{}'
        )
        obj.delete()
        assert mock_request.call_count == 2

    @patch('txlib.http.http_requests.requests.request')
    def test_saving_new_object_creates_it(self, mock_request):
        mock_request.return_value = get_mock_response(
            200, '{"id": 100, "description": "description"}'
        )

        # Method 1: set attributes, then save()
        obj = DummyModel(slug='slug')
        obj.name = 'name'
        obj.description = 'description'
        obj.save()
        assert obj.name == 'name'
        assert obj.description == 'description'

        # Method 2: save() at once with all attributes
        obj = DummyModel(slug='slug')
        obj.save(
            name='name',
            description='description'
        )
        assert obj.name == 'name'
        assert obj.description == 'description'

    def test_exception_if_setting_wrong_url_field(self):
        with pytest.raises(AttributeError) as excinfo:
            BaseModel(invalid='anything')
        assert 'BaseModel has no URL attribute "invalid"' == \
               excinfo.value.args[0]

        with pytest.raises(AttributeError):
            BaseModel(slug='slug', invalid='anything')
        assert 'BaseModel has no URL attribute "invalid"' == \
               excinfo.value.args[0]

    def test_exception_if_omitting_url_field(self):
        with pytest.raises(AttributeError) as excinfo:
            DummyModel.get()
        assert 'DummyModel has no URL attribute "slug"' == \
               excinfo.value.args[0]

    def test_exception_if_retrieving_invalid_attribute(self):
        b = DummyModel(slug='slug')
        with pytest.raises(AttributeError) as excinfo:
            b.invalid
        assert 'DummyModel has no readable attribute "invalid"' == \
               excinfo.value.args[0]

        # Existing attribute should work, however
        assert b.slug == 'slug'

    def test_exception_when_saving_invalid_field(self):
        """Invalid fields should raise an exception when save() is called."""

        obj = DummyModel()
        with pytest.raises(AttributeError) as excinfo:
            obj.save(
                name='name',
                description='description',
                invalid='anything'
            )

        assert 'DummyModel has no writable attribute "invalid"' == \
               excinfo.value.args[0]

    def test_exception_when_handling_wrong_field(self):
        """The _handle_wrong_field() method should raise an exception if
        an invalid attribute is provided."""

        obj = DummyModel()
        with pytest.raises(AttributeError) as excinfo:
            obj._handle_wrong_field('anything', 'yo')

        assert 'Invalid attribute type: yo' == excinfo.value.args[0]
