# -*- coding: utf-8 -*-

"""
String translation wrapper.
"""

import json

from txlib.api.base import BaseModel
from txlib.api.exceptions import MissingArgumentsError
from hashlib import md5

class StringTranslationObjectsHandlernslations(BaseModel):
	"""Model class for String Transaltions."""


   	_path_to_collection = None 
	_path_to_item = 'project/%(project_slug)s/resource/%(slug)s/translation/%(lang)s/strings/'
	
	read_only_fields = set(['content', ])
	write_also_fields = set(['content', ])
	mandatory_fields = set(['content', ])
	url_fields = set(['project_slug', 'slug', 'lang', ])
