# -*- coding: utf-8 -*-

"""
Resource wrapper.
"""

import json

from txlib.api.base import BaseModel
from txlib.api.exceptions import MissingArgumentsError


class Resource(BaseModel):
    """Model class for resources."""

    _path_to_collection = 'project/%(project_slug)s/resources/'
    _path_to_item = 'project/%(project_slug)s/resource/%(slug)s/?details'
    _path_to_source_language = 'project/%(project_slug)s/resource/%(slug)s/content/'

    read_only_fields = set([
        'slug', 'name', 'created', 'available_languages', 'mimetype',
        'source_language_code', 'project_slug', 'wordcount', 'total_entities',
        'accept_translations', 'last_update',
    ])
    write_also_fields = set([
        'slug', 'name', 'accept_translations', 'source_language',
        'mimetype', 'content', 'i18n_type',
    ])
    mandatory_fields = set(['slug', 'name', 'mimetype', ])
    url_fields = set(['project_slug', 'slug', ])

    def __getattr__(self, name):
        """Make separate handling of the content of a resource."""
        if name == 'content':
            path = self._construct_path_to_source_content()
            res = self._http.get(path)
            self._populated_fields['content'] = res['content']
            return res['content']
        return super(Resource, self).__getattr__(name)

    def _update(self, **kwargs):
        """Use separate URL for updating the source file."""
        if 'content' in kwargs:
            content = kwargs.pop('content')
            path = self._construct_path_to_source_content()
            self._http.put(path, json.dumps({'content': content}))
        super(Resource, self)._update(**kwargs)

    def _construct_path_to_source_content(self):
        """Construct the path to the source content for an actual resource."""
        return self.path_to_source_content_template % self.url_parameters

    @property
    def path_to_source_content_template(self):
        """Return the path to the source language content."""
        return self._join_subpaths(self._prefix, self._path_to_source_language)
