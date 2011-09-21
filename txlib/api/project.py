# -*- coding: utf-8 -*-

"""
Project wrapper.
"""

from txlib.utils import _logger
from txlib.api.base import BaseModel
from txlib.api.exceptions import MissingArgumentsError


class Project(BaseModel):
    """Model class for projects."""

    _path_to_collection = 'projects/'
    _path_to_item = 'project/%(slug)s/?details'

    read_only_fields = set([
        'slug', 'name', 'description', 'long_description', 'homepage', 'feed',
        'created', 'anyone_submit', 'bug_tracker', 'trans_instructions',
        'tags', 'maintainers', 'outsource', 'owner', 'resources',
    ])
    write_also_fields = set([
        'slug', 'name', 'description', 'long_description', 'private',
        'homepage', 'feed', 'anyone_submit', 'hidden', 'bug_tracker',
        'trans_instructions', 'tags', 'maintainers', 'outsource',
    ])
    mandatory_fields = set(['slug', 'name', 'owner', ])
    url_fields = set(['slug', ])
