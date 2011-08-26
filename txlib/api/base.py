# -*- coding: utf-8 -*-

from txib.utils import _logger
from txlib.registry import registry


class BaseModel(object):
    """Base class for Tx models.

    Each model has a list of fields. The model works as a proxy between the
    local application and the remote Tx server.

    The user of the class can either create a local-only instance using the
    staticmethod ``get`` or retrieve a remote object whenever he accesses
    an attribute that has no value.
    """

    fields = []

    @staticmethod
    def get(self, *args, **kwargs):
        """Method to retrieve an object from a Tx server."""
        pass

    def __init__(self, prefix='/api/2/', *args, **kwargs):
        """Initializer.

        Args:
            prefix: The prefix of the urls.
        """
        self._prefix = prefix

    def _populate(self):
        """Populate the isntance with the values from the server."""
        pass


class BaseBackend(object):
    """Base class for Tx models backend.

    Each backend allows to get, create, edit and delete a resource.
    """

    _prefix = '/api/2/'
    _path_to_collection = ''    # shouldn't start with a slash
    _path_to_item = ''          # shouldn't start with a slash

    def __init__(self):
        """Initializer.

        Setup the http handler.
        """
        self.http = registry.http_handler

    def get(self, **kwargs):
        """Get the resource from a remote Tx server."""
        (path, kwargs) = self._construct_path_to_item(**kwargs)
        return self.http.get(path)

    def create(self):
        """Create a resource in the remote Tx server."""
        (path, kwargs) = self._construct_path_to_collection(**kwargs)
        return self.http.post(path, kwargs)

    def edit(self):
        """Edit a resource in a remote Tx server."""
        (path, kwargs) = self._construct_path_to_item(**kwargs)
        return self.http.put(path, kwargs)

    def delete(self):
        """Delete a resource from a remote Tx server."""
        (path, kwargs) = self._construct_path_to_item(**kwargs)
        return self.http.delete(path, kwargs)

    def _construct_path_to_collection(self, **kwargs):
        """Construct the path to an actual collection."""
        raise NotImplementedError

    def _construct_path_to_item(self, **kwargs):
        """Construct the path to an actual item."""
        raise NotImplementedError

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

