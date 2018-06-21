# -*- coding: utf-8 -*-

from txlib.api.base import BaseModel


class Translation(BaseModel):
    """Model class for translations."""

    _path_to_item = 'project/%(project_slug)s/resource/%(slug)s/translation/%(lang)s'  # noqa
    _path_to_collection = None

    writable_fields = {'content'}
    url_fields = {'project_slug', 'slug', 'lang'}
