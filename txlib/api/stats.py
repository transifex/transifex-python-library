# -*- coding: utf-8 -*-

"""
Stats wrapper.
"""

from txlib.api.base import BaseModel


class Stats(BaseModel):
    """Model class for translations."""

    _path_to_item = 'project/%(project_slug)s/resource/%(slug)s/stats/%(lang)s/'
    _path_to_collection = 'project/%(project_slug)s/resource/%(slug)s/stats/'

    read_only_fields = set([
            'completed', 'translated_entities', 'untranslated_entities',
            'translated_words', 'untranslated_words', 'last_update',
            'last_committer', 'reviewed', 'reviewed_percentage',
    ])
    write_also_fields = set([])
    mandatory_fields = set([])
    url_fields = set(['project_slug', 'slug', 'lang', ])
