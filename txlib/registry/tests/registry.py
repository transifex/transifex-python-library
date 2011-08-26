# -*- coding: utf-8 -*-


from txlib.utils.imports import unittest
from txlib.registry.registry import _Registry
from txlib.http.auth import AnonymousAuth, BasicAuth


class TestRegistry(unittest.TestCase):
    """Tests for the Registry class."""

    @classmethod
    def setUpClass(cls):
        """Save the default responsibilities of the registry."""
        cls.default_responsibilities = _Registry.responsibilities.copy()

    def setUp(self):
        self.r = _Registry()
        self.r.responsibilities = self.default_responsibilities.copy()

    def test_get_unknown_responsibility(self):
        """Test wrong responsibilities."""
        self.assertIs(self.r.wrong, None)

    def test_get_responsibility(self):
        """Test fetching the class for a responsibility."""

        class TestResponsibility(object):
            pass

        self.r.responsibilities['test'] = TestResponsibility
        self.assertIs(self.r.test, TestResponsibility)

    def test_setup(self):
        """Test the setup of a responsibility object."""
        self.r.setup({'new': 'new'})
        self.assertEquals(len(self.r.responsibilities.keys()), 1)
        self.assertEquals(self.r.new, 'new')
        self.r.setup({'auth_class': AnonymousAuth})
        self.assertEquals(len(self.r.responsibilities.keys()), 2)
        self.assertEquals(self.r.auth_class, AnonymousAuth)
        self.r.setup({'auth_class': BasicAuth, 'newnew': 'newnew'})
        self.assertEquals(len(self.r.responsibilities.keys()), 3)
        self.assertEquals(self.r.auth_class, BasicAuth)
        self.assertEquals(self.r.newnew, 'newnew')
