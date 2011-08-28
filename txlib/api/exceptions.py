# -*- coding: utf-8 -*-
"""
A collection of exceptions used in txlib.api.
"""


class ApiError(Exception):
    """Base class for API errors."""


class MissingArgumentsError(ApiError):
    """Exception used when arguments are missing."""
