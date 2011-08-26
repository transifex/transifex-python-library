# -*- coding: utf-8 -*-

from txlib.utils import _logger
from txlib.registry.exceptions import DoesNotExist
from txlib.http.auth import BasicAuth
from txlib.http.http_requests import HttpRequest


class _Registry(object):
    """A class to act as registry for the various objects used.

    This is used to decouple various classes and allows finer-grained split of
    responsibilities to classes.
    """

    responsibilities = {
        'auth_class': BasicAuth,
        'http_handler': HttpRequest,
    }

    def __getattr__(self, name):
        """Return the class for the various responsibilities."""
        if name in self.responsibilities:
            return self.responsibilities[name]
        else:
            msg = "Responsibility '%s' does not exist." % name
            _logger.warning(msg)
            raise DoesNotExist(msg)

    def setup(self, responsibilities):
        """Initial setup of the responsibilities.

        Allows to override the defaults and/or add new ones.

        Args:
            `responsibilities`: A dictionary of responsibilities to define.
        """
        self.responsibilities.update(responsibilities)
