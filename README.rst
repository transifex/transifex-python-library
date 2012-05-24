==========================
 Transifex Python Library
==========================

The library is a wrapper around the Transifex API that tries to present
a simpler interface to the developers.

Installation & Requirements
===========================

To install the latest version of the library
::
 pip install -e 'git://github.com/transifex/transifex-python-library#egg=txlib'

The required python packages will be automatically installed.

Quick Howto
===========

Setting up the connection:
  >>> from txlib.registry import registry
  >>> from txlib.http.auth import BasicAuth
  >>> from txlib.http.http_requests import HttpRequest
  >>> cred = BasicAuth(username='<username>', password='<password>')
  >>> conn = HttpRequest('<transifex_host>', auth=cred)
  >>> registry.setup({'http_handler': conn})

Creating a project:
  >>> from txlib.api.project import Project
  >>> p = Project()
  >>> p.slug = '<project_slug>'
  >>> p.name = 'A project'
  >>> p.description = 'Sample project for demonstration purposes'
  >>> p.source_language_code = 'en'
  >>> p.save()

Creating a resource:
  >>> r = Resource(project_slug='<project_slug>', slug='<resource_slug>')
  >>> r.name = 'Resource name'
  >>> r.i18n_type = 'PO'
  >>> content = open(filename, 'r')
  >>> r.content = content.read()
  >>> content.close()
  >>> r.save()

Creating a resource the safe way:
  >>> from txlib.http.exceptions import *
  >>> from txlib.api.resources import Resource
  >>> try:
  >>>     r = Resource().get(project_slug='<project_slug>', slug='<resource_slug>')
  >>> except NotFoundError:
  >>>     r = Resource(project_slug='<project_slug>', slug='<resource_slug>')
  >>>     r.name = 'Resource name'
  >>>     r.i18n_type = 'PO'
  >>>     content = open(filename, 'r')
  >>>     r.content = content.read()
  >>>     content.close()
  >>>     r.save()

Creating or Updating a translation:
  >>> from txlib.api.translations import Translation
  >>> t = Translation(project_slug = '<project_slug>', slug = '<resource_slug>', lang = 'el_GR')
  >>> content = open(localized_filename,'r')
  >>> t.content = content.read()
  >>> content.close()
  >>> t.save()

Downloading a translation:
  >>> from txlib.api.translations import Translation
  >>> t = Translation(project_slug = '<project_slug>', slug = '<resource_slug>', lang = 'el_GR')
  >>> trans = open(localized_filename,'w')
  >>> strings = t.content
  >>> trans.write(strings.encode('UTF-8'))
  >>> trans.close()

Deleting an object (eg. a project):
  >>> from txlib.api.project import Project
  >>> p = Project().get(slug='<project_slug>')
  >>> p.delete()

Getting a property (eg. the wordcount of a resource):
  >>> from txlib.api.resources import Resource
  >>> r = Resource().get(project_slug='<project_slug>', slug='<resource_slug>')
  >>> print 'Words in the resource: %s' % r.wordcount

Exceptions
==========

=================================     ====================================================================
txlib.api.MissingArgumentsError       Exception used when API arguments are missing.
txlib.http.RequestError               This is a 400 error.
txlib.http.NotFoundError              This is for 404 errors
txlib.http.AuthenticationError        This is a 403 error.
txlib.http.AuthorizationError         This is a 401 error.
txlib.http.ConflictError              This is a 409 error.
txlib.http.UnknownError               Class for errors which are not handled specifically.
txlib.http.RemoteServerError          Class for 5xx errors.
txlib.http.NoResponseError            Exception raised when there was no connection to the remopte server.
=================================     ====================================================================


Question/Issues
===============
For general questions, you can email us at: transifex-devel [at] googlegroups [dot] com

To report issues, you can use https://github.com/transifex/transifex-python-library/issues

---------------------

Copyright (c) 2012, Indifex, Inc.
See the files COPYING and COPYING.LESSER for copyright information
concerning this distribution and all its components.
