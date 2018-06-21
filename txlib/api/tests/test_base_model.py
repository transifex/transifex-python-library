# -*- coding: utf-8 -*-
import pytest
from txlib.api.base import BaseModel


class TestBaseModel():
    """Test the base model for the Transifex model wrappers."""

    def test_join_subpaths(self):
        """Test that subpaths are joined correctly."""
        b = BaseModel()
        correct_path = '/api/2/projects/'

        # all subpaths have slashes
        path = b._join_subpaths('/api/', '/2/', '/projects/')
        assert path.count('/') == 4
        assert path == correct_path

        # none subpath has slashes
        path = b._join_subpaths('/api', '2', 'projects/')
        assert path.count('/') == 4
        assert path == correct_path

        # there are some slashes
        path = b._join_subpaths('/api/', '2/', 'projects/')
        assert path.count('/') == 4
        assert path == correct_path
