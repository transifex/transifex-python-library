# -*- coding: utf-8 -*-

"""
Resource wrapper.
"""

from txlib.api.base import BaseModel
from txlib.api.exceptions import MissingArgumentsError


class Resource(BaseModel):
    """Model class for resources."""

    _path_to_collection = 'project/%(project_slug)s/resources/'
    _path_to_item = 'project/%(project_slug)s/resource/%(slug)s/?details'

    read_only_fields = set([
        'slug', 'name', 'created', 'available_languages', 'mimetype',
        'source_language_code', 'project_slug', 'wordcount', 'total_entities',
        'accept_translations', 'last_update',
    ])
    write_also_fields = set([
        'slug', 'name', 'accept_translations', 'source_language',
        'mimetype', 'content',
    ])
    mandatory_fields = set(['slug', 'name', 'mimetype', ])
    url_fields = set(['project_slug', 'slug', ])
