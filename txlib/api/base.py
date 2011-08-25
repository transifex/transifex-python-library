# -*- coding: utf-8 -*-


class BaseModel(object):
    """Base class for Tx models.

    Each model has a list of fields. The model works as a proxy between the
    local application and the remote Tx server.
    """

    fields = []

    _prefix = '/api/2/'
    _path_to_collection = ''    # shouldn't start with a slash
    _path_to_item = ''          # shouldn't start with a slash

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

    @property
    def path_to_collection(self):
        """The URL to access the collection of the model."""
        return self._join_subpaths(self._prefix, self._path_to_collection)

    @property
    def path_to_item(self):
        """The URL to access a specific item of the model."""
        return self._join_subpaths(self._prefix, self._path_to_item)

    def _join_subpaths(self, *args):
        """Join subpaths (given as arguments) to form a
        well-defined URL path.
        """
        return '/'.join(args).replace('///', '/').replace('//', '/')


