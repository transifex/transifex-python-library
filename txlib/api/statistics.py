# -*- coding: utf-8 -*-

"""
Statistics wrapper.
"""

import json

from txlib.api.base import BaseModel
from txlib.api.exceptions import MissingArgumentsError


class Statistics(BaseModel):
    """Model class for statistics."""

    _path_to_item = '/project/%(project_slug)s/resource/%(resource_slug)s/stats/'

    read_only_fields = set([
        'completed', 'translated_entities', 'untranslated_entities',
        'translated_words', 'untranslated_words', 'last_update',
        'last_committer', 'reviewed', 'reviewed_percentage',
    ])
    #write_also_fields = set([])
    #mandatory_fields = set(['project_slug', 'resource_slug', ])
    url_fields = set(['project_slug', 'resource_slug', 'lang_code'])
