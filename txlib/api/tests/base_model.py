# -*- coding: utf-8 -*-

from txlib.utils.imports import unittest
from txlib.api.base import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test the base model for the Tx model wrappers."""

    def test_join_subpaths(self):
        """Test that subpaths are joined correctly."""
        b = BaseModel()
        correct_path = '/api/2/projects/'

        # all subpaths have slashes
        path = b._join_subpaths('/api/', '/2/', '/projects/')
        self.assertEquals(path.count('/'), 4)
        self.assertEquals(path, correct_path)

        # none subpath has slashes
        path = b._join_subpaths('/api', '2', 'projects/')
        self.assertEquals(path.count('/'), 4)
        self.assertEquals(path, correct_path)

        # there are some slashes
        path = b._join_subpaths('/api/', '2/', 'projects/')
        self.assertEquals(path.count('/'), 4)
        self.assertEquals(path, correct_path)

