# -*- coding: utf-8 -*-
"""
The http library of the module.

The module provides the necessary classes and functions to perform http calls.

"""

import sys
if sys.version_info < (2, 6):
    import simplejson as json
else:
    import json
