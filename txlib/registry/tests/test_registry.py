# -*- coding: utf-8 -*-
import pytest

from txlib.registry.registry import _Registry
from txlib.http.auth import AnonymousAuth, BasicAuth


class TestRegistry():
    """Tests for the Registry class."""

    @pytest.fixture(autouse=True)
    def auto_init(self):
        """Save the default responsibilities of the registry."""
        self.default_responsibilities = _Registry.responsibilities.copy()
        self.r = _Registry()
        self.r.responsibilities = self.default_responsibilities.copy()

    def test_get_unknown_responsibility(self):
        """Test wrong responsibilities."""
        assert self.r.wrong is None

    def test_get_responsibility(self):
        """Test fetching the class for a responsibility."""

        class TestResponsibility(object):
            pass

        self.r.responsibilities['test'] = TestResponsibility
        assert self.r.test is TestResponsibility

    def test_setup(self):
        """Test the setup of a responsibility object."""
        self.r.setup({'new': 'new'})
        assert len(self.r.responsibilities.keys()) == 1
        assert self.r.new == 'new'

        self.r.setup({'auth_class': AnonymousAuth})
        assert len(self.r.responsibilities.keys()) == 2
        assert self.r.auth_class == AnonymousAuth

        self.r.setup({'auth_class': BasicAuth, 'newnew': 'newnew'})
        assert len(self.r.responsibilities.keys()) == 3
        assert self.r.auth_class == BasicAuth
        assert self.r.newnew == 'newnew'

    def test_remove(self):
        """Test the removal of a responsibility object."""
        self.r.setup({'one': 1, 'two': 2, 'three': 3})
        assert len(self.r.responsibilities.keys()) == 3

        self.r.remove('one')
        assert len(self.r.responsibilities.keys()) == 2

        self.r.remove('two')
        assert len(self.r.responsibilities.keys()) == 1

        self.r.remove('three')
        assert len(self.r.responsibilities.keys()) == 0

