# -*- coding: utf-8 -*-
import json

from txlib.api.base import BaseModel


class Translation(BaseModel):
    """Model class for translations."""

    _path_to_item = 'project/%(project_slug)s/resource/%(slug)s/translation/%(lang)s'  # noqa
    _path_to_collection = 'project/%(project_slug)s/resource/'\
                          '%(slug)s/translation/%(lang)s'

    writable_fields = {'content'}
    url_fields = {'project_slug', 'slug', 'lang'}

    def _create(self, **kwargs):
        """Create the translation of a resource.

        The _create function differentiates from the one in the BaseModel
        in the HTTP request that takes place in the end. In the Translation
        object's case, it needs to be `PUT`, while in the BaseModel is `POST`
        """
        path = self._construct_path_to_collection()

        # Use the fields for which we have values
        for field in self.writable_fields:
            try:
                value = getattr(self, field)
                kwargs[field] = value
            except AttributeError:
                pass
        return self._http.put(path, json.dumps(kwargs))
