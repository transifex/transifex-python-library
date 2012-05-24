# -*- coding: utf-8 -*-

"""
Translations wrapper.
"""

from txlib.api.base import BaseModel
from txlib.api.exceptions import MissingArgumentsError


class Translation(BaseModel):
    """Model class for translations."""

    _path_to_item = 'project/%(project_slug)s/resource/%(slug)s/translation/%(lang)s/'
    _path_to_collection = None

    read_only_fields = set(['content', ])
    write_also_fields = set(['content', ])
    mandatory_fields = set(['content', ])
    url_fields = set(['project_slug', 'slug', 'lang', ])

    def save(self):
        """Save the instance to the remote Transifex server.

        The translations use only PUT requests, so use the _update
        method of the parent class.
        """
        self._update(**self._modified_fields)
