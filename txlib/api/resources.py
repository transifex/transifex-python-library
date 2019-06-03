# -*- coding: utf-8 -*-

"""
Resource wrapper.
"""

import json

from txlib.api.base import BaseModel


class Resource(BaseModel):
    """Model class for resources."""

    _path_to_collection = 'project/%(project_slug)s/resources/'
    _path_to_item = 'project/%(project_slug)s/resource/%(slug)s/?details'
    _path_to_source_language = 'project/%(project_slug)s/resource/' \
                               '%(slug)s/content/'

    writable_fields = {
        'slug', 'name', 'accept_translations', 'source_language',
        'mimetype', 'content', 'i18n_type', 'categories', 'category',
        'metadata',
    }
    url_fields = {'project_slug', 'slug'}

    def retrieve_content(self):
        """Retrieve the content of a resource."""
        path = self._construct_path_to_source_content()
        res = self._http.get(path)
        self._populated_fields['content'] = res['content']
        return res['content']

    def _create(self, **kwargs):
        """Create a resource in the remote Transifex server."""
        path = self._construct_path_to_collection()
        content = kwargs['content']
        is_binary = not isinstance(content, str)

        # Use the fields for which we have values
        for field in self.writable_fields:
            try:
                value = getattr(self, field)
                kwargs[field] = value
                # on binary files pass the content as a separate
                # parameter (not in kwargs)
                if field == 'content' and is_binary:
                    kwargs.pop('content', None)
            except AttributeError:
                pass

        if is_binary:
            return self._http.post(path, kwargs, content)

        return self._http.post(path, json.dumps(kwargs))

    def _update(self, **kwargs):
        """Use separate URL for updating the source file."""
        if 'content' in kwargs:
            content = kwargs.pop('content')
            path = self._construct_path_to_source_content()
            is_binary = not isinstance(content, str)
            if not is_binary:
                self._http.put(path, json.dumps({'content': content}))
            else:
                self._http.put(path, kwargs, content)
        super(Resource, self)._update(**kwargs)

    def _construct_path_to_source_content(self):
        """Construct the path to the source content for an actual resource."""
        template = self.get_path_to_source_content_template()  # flake8 fix
        return template % self.get_url_parameters()

    def get_path_to_source_content_template(self):
        """Return the path to the source language content."""
        return self._join_subpaths(self._prefix, self._path_to_source_language)

    def __str__(self):
        return '[Resource slug={}]'.format(self.slug)
