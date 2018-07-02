# -*- coding: utf-8 -*-

"""
Project wrapper.
"""

from txlib.api.base import BaseModel


class Project(BaseModel):
    """Model class for projects."""

    _path_to_collection = 'projects/'
    _path_to_item = 'project/%(slug)s/?details'

    writable_fields = {
        'slug', 'name', 'description', 'long_description', 'private',
        'homepage', 'feed', 'anyone_submit', 'hidden', 'bug_tracker',
        'trans_instructions', 'tags', 'maintainers', 'outsource',
        'source_language_code',
    }
    url_fields = {'slug'}

    def __str__(self):
        return '[Project slug={}]'.format(self.slug)
