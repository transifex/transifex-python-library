# -*- coding: utf-8 -*-

"""
Registry package for the txlib.

This package allows the user of the package to change the classes and functions
used in txlib, so that he can easily change the implementations used in various
parts.
"""

from txlib.registry.registry import _Registry
registry = _Registry()
