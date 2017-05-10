# -*- coding: utf-8 -*-
"""
The txlib package.
"""

__version__ = '0.1.0'
__author__ = 'Indifex Ltd. <info@indifex.com>'
__all__ = []

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
