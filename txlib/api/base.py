# -*- coding: utf-8 -*-
"""Contains a base model class, the subclasses of which represent
models on the Transifex core.

The BaseModel class works as a framework for performing all necessary
CRUD operations for its subclasses. The subclasses typically only need
to define a set of configuration parameters (such as the expected fields
for retrieving objects, or the parameters that can be modified on an object).
For any custom functionality, subclasses may have to add override existing
functions.

Examples:
The examples below do not handle exceptions. You can find more detailed
examples in the README.

# Retrieve object
>>> obj = MyModel.get(attr1='value1', attr2='value2')

# Create object
>>> obj = MyModel(attr1='value1', attr2='value2')
>>> obj.save(
>>>     param1='...',
>>>     param2='...',
>>>     extra_param='...',
>>> )
>>> # Alternatively:
>>> obj = MyModel(attr1='value1', attr2='value2')
>>> obj.param1 = '...'
>>> obj.param2 = '...'
>>> obj.extra_param = '...'
>>> obj.save()

# Update object
>>> obj = MyModel.get(attr1='value1', attr2='value2')
>>> obj.save(
>>>     param1='...',
>>>     param2='...',
>>> )
>>> # Alternatively
>>> obj = MyModel.get(attr1='value1', attr2='value2')
>>> obj.param1 = '...'
>>> obj.param2 = '...'
>>> obj.save()
"""


import json

from txlib.utils import _logger
from txlib.registry import registry


class BaseModel(object):
    """Base class for Transifex models.

    Each model has a list of fields. The model works as a proxy between the
    local application and the remote Transifex server.

    The user of the class can:
      a) retrieve an existing remote instance of the model
         by using the static method `MyModel.get(...)`
      b) create a new local instance with a set of populated fields
         and call `save()` in order to save it to the remote server
      c) delete an existing remote instance, by first creating a local instance
         and all necessary attributes that identify the object, and then
         calling `delete()` on it.
    """

    # The URI prefix of all API endpoints for this model
    _prefix = ''

    # The URI for retrieving a collection of multiple items
    # (shouldn't start with a slash)
    _path_to_collection = ''

    # The URl for retrieving a single item
    # (shouldn't start with a slash)
    _path_to_item = ''

    # All fields defined here will be used for constructing
    # the URL of the request
    url_fields = set()

    # These fields can be modified in POST/PUT requests
    writable_fields = set()

    # Initially False, set to True when an instance of the class is created
    _is_initialized = False

    @classmethod
    def get(cls, **kwargs):
        """Retrieve an object by making a GET request to Transifex.

        Each value in `kwargs` that corresponds to a field
        defined in `self.url_fields` will be used in the URL pth
        of the request, so that a particular entry of this model
        is identified and retrieved.

        Raises:
            txlib.http.exceptions.NotFoundError: if the object with these
                attributes is not found on the remote server
            txlib.http.exceptions.ServerError subclass: depending on
                the particular server response

        Example:
        # Note: also catch exceptions
        >>> obj = MyModel.get(attr1=value1, attr2=value2)
        """
        fields = {}
        for field in cls.url_fields:
            fields[field] = kwargs.pop(field, None)

        # Create an instance of the model class and make the GET request
        model = cls(**fields)
        model._populate(**kwargs)
        return model

    def __init__(self, prefix='/api/2/', **url_values):
        """Constructor.

        Initializes various variables, setup the HTTP handler and
        stores all values

        Args:
            prefix: The prefix of the urls.
        """
        self._http = registry.http_handler
        self._prefix = prefix
        self._modified_fields = {}
        self._populated_fields = {}

        for field in url_values:
            if field in self.url_fields:
                setattr(self, field, url_values[field])
            else:
                self._handle_wrong_field(field)

        # From now on only, only specific attributes can be set
        # on this object:
        #  a) one of the instance variables set above
        #  b) one of the attributes found in `self.writable_fields`
        self._is_initialized = True

    def __getattr__(self, name, default=None):
        """Return the value of the field with the given name.

        Looks in `self._modified_fields` and `self._populated_fields`.

        Raises an AttributeError if the requested attribute does not exist.
        """
        if name in self._modified_fields:
            return self._modified_fields[name]

        elif name in self._populated_fields:
            return self._populated_fields[name]

        else:
            self._handle_wrong_field(name)

    def __setattr__(self, name, value):
        """Set the value of a field.

        This method only allows certain attributes to be set:
          a) Any attribute that is defined in `__init__()`
          b) Any attribute found in `self.writable_fields`

        For the rest it will raise an AttributeError.

        For case (a), the attribute is saved directly on this object
        For case (b), the attribute is saved in `self.writable_fields`
        """
        # If __init__() hasn't finished yet, accept anything
        if ('_is_initialized' not in self.__dict__) or (name in self.__dict__):
            return super(BaseModel, self).__setattr__(name, value)

        elif name in self.writable_fields:
            self._modified_fields[name] = value

        else:
            self._handle_wrong_field(name)

    def save(self, **fields):
        """Save the instance to the remote Transifex server.

        If it was pre-populated, it updates the instance on the server,
        otherwise it creates a new object.

        Any values given in `fields` will be attempted to be saved
        on the object. The same goes for any other values already set
        to the object by `model_instance.attr = value`.

        Raises:
            AttributeError: if a given field is not included in
                `self.writable_fields`,
        """
        for field in fields:
            if field in self.writable_fields:
                setattr(self, field, fields[field])
            else:
                self._handle_wrong_field(field)

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
        """Get the resource from a remote Transifex server."""
        path = self._construct_path_to_item()
        return self._http.get(path)

    def _create(self, **kwargs):
        """Create a resource in the remote Transifex server."""
        path = self._construct_path_to_collection()

        # Use the fields for which we have values
        for field in self.writable_fields:
            try:
                value = getattr(self, field)
                kwargs[field] = value
            except AttributeError:
                pass
        return self._http.post(path, json.dumps(kwargs))

    def _update(self, **kwargs):
        """Update a resource in a remote Transifex server."""
        path = self._construct_path_to_item()
        if not kwargs:
            return
        return self._http.put(path, json.dumps(kwargs))

    def _delete(self, **kwargs):
        """Delete a resource from a remote Transifex server."""
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
        """Create a dictionary of parameters used in URLs for this model."""
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

    def _handle_wrong_field(self, field_name):
        """Raise an exception whenever an invalid attribute with
        the given name was attempted to be set to or retrieved from
        this model class.

        Assumes that the given field is invalid, without making any checks.

        Also adds an entry to the logs.
        """
        msg = "%s has no attribute %s" % (self.__class__.__name__, field_name)
        _logger.error(msg)
        raise AttributeError(msg)

class LegacyModel(BaseModel):
    """Base class for Transifex models in the old v2 API."""
    _prefix = '/api/2/'
