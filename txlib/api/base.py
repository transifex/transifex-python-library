# -*- coding: utf-8 -*-

from txlib.utils import _logger
from txlib.utils.imports import json
from txlib.registry import registry


class BaseModel(object):
    """Base class for Tx models.

    Each model has a list of fields. The model works as a proxy between the
    local application and the remote Tx server.

    The user of the class can either create a local-only instance using the
    staticmethod ``get`` or retrieve a remote object whenever he accesses
    an attribute that has no value.
    """

    _prefix = '/api/2/'
    _path_to_collection = ''    # shouldn't start with a slash
    _path_to_item = ''          # shouldn't start with a slash

    read_only_fields = set()
    write_also_fields = set()
    mandatory_fields = set()
    fields = read_only_fields | write_also_fields
    url_fields = {}

    @classmethod
    def get(cls, **kwargs):
        """Method to retrieve an object from a Tx server."""
        url_fields = {}
        for field in cls.url_fields:
            url_fields[field] = kwargs.pop(field, None)
        model = cls(**url_fields)
        model._populate(**kwargs)
        return model

    def __init__(self, prefix='/api/2/', **kwargs):
        """Initializer.

        Setupo the http handler, too.

        Args:
            prefix: The prefix of the urls.
        """
        self._http = registry.http_handler
        self._prefix = prefix
        self._modified_fields = {}
        self._populated_fields = {}
        for field in self.url_fields:
            if field in kwargs:
                setattr(self, field, kwargs[field])
        self._is_initialized = True

    def __getattr__(self, name):
        """Return the value of the field.

        Look in the modified and the populated fields.
        """
        if name in self._modified_fields:
            return self._modified_fields[name]
        elif name in self._populated_fields:
            return self._populated_fields[name]
        else:
            msg = "%s has no attribute %s" % (self.__class__.__name__, name)
            _logger.error(msg)
            raise AttributeError(msg)

    def __setattr__(self, name, value):
        """Set the value of a field."""
        if not '_is_initialized' in self.__dict__ or name in self.__dict__:
            return super(BaseModel, self).__setattr__(name, value)
        elif name in self.write_also_fields:
            self._modified_fields[name] = value
        else:
            msg = "%s has no attribute %s" % (self.__class__.__name__, name)
            _logger.error(msg)
            raise AttributeError(msg)

    def save(self):
        """Save the instance to the remote Transifex server.

        If it was pre-populated, then update the instance in the server.
        Else create a new instance.
        """
        if self._populated_fields:
            self._update(**self._modified_fields)
        else:
            self._create(**self._modified_fields)

    def delete(self):
        """Delete the instance from the remote Transifex server."""
        self._delete()

    def _populate(self, **kwargs):
        """Populate the instance with the values from the server."""
        self._populated_fields = self._get(**kwargs)

    def _get(self, **kwargs):
        """Get the resource from a remote Tx server."""
        path = self._construct_path_to_item()
        return self._http.get(path)

    def _create(self, **kwargs):
        """Create a resource in the remote Tx server."""
        path = self._construct_path_to_collection()
        for field in self.url_fields:
            kwargs[field] = getattr(self, field)
        return self._http.post(path, json.dumps(kwargs))

    def _update(self, **kwargs):
        """Update a resource in a remote Tx server."""
        path = self._construct_path_to_item()
        if not kwargs:
            return
        return self._http.put(path, json.dumps(kwargs))

    def _delete(self, **kwargs):
        """Delete a resource from a remote Tx server."""
        path = self._construct_path_to_item()
        return self._http.delete(path)

    def _construct_path_to_collection(self):
        """Construct the path to an actual collection."""
        return self.path_to_collection_template % self.url_parameters

    def _construct_path_to_item(self):
        """Construct the path to an actual item."""
        return self.path_to_item_template % self.url_parameters

    @property
    def url_parameters(self):
        """Create a dictionary of the parameters used in URLs for this model."""
        url_fields = {}
        for field in self.url_fields:
            url_fields[field] = getattr(self, field)
        return url_fields

    @property
    def path_to_collection_template(self):
        """The URL to access the collection of the model."""
        return self._join_subpaths(self._prefix, self._path_to_collection)

    @property
    def path_to_item_template(self):
        """The URL to access a specific item of the model."""
        return self._join_subpaths(self._prefix, self._path_to_item)

    def _join_subpaths(self, *args):
        """Join subpaths (given as arguments) to form a
        well-defined URL path.
        """
        return '/'.join(args).replace('///', '/').replace('//', '/')
