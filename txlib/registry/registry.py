# -*- coding: utf-8 -*-

from txlib.utils import _logger
from txlib.http.auth import AnonymousAuth
from txlib.http.http_requests import HttpRequest


class _Registry(object):
    """A class to act as registry for the various objects used.

    This is used to decouple various classes and allows finer-grained split of
    responsibilities to classes.
    """

    responsibilities = {}

    def __getattr__(self, name):
        """Return the class for the various responsibilities."""
        res = self.responsibilities.get(name, None)
        if res is None:
            msg = "Responsibility '%s' does not exist." % name
            _logger.warning(msg)
        return res

    def setup(self, responsibilities):
        """Initial setup of the responsibilities.

        Allows to override the defaults and/or add new ones.

        Args:
            `responsibilities`: A dictionary of responsibilities to define.
        """
        self.responsibilities.update(responsibilities)
