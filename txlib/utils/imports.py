# -*- coding: utf-8 -*-

"""
Define shortcuts to various imports needed.
"""

import sys
if sys.version_info < (2, 6):
    import simplejson as json
else:
    import json


import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
