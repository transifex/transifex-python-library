==========================
 Transifex Python Library
==========================

The library is a wrapper around the Transifex API that tries to present
a simpler interface to the developers.

It is used to make transifex API alive. It has the base class for tx models. Each model has a list of fields. The model works as a proxy between the local tx application and the remote tx server. The user can create a local-only instance or retrieve a remote object whenever he accesses an attribute that has no value.

 

Installation & requirements

 

To install the latest version of the library you can give the command below

pip install -e 'git://github.com/transifex/transifex-python-library#egg=txlib'
 

All the required python packages will be automatically installed.
 

Setting up the connection
 

>>> from txlib.registry import registry
>>> from txlib.http.auth import BasicAuth
>>> from txlib.http.http_requests import HttpRequest
 

>>> d = BasicAuth(username='<username>', password='<password>')
 

The returned value depends on the arguments given, In case the username and password are empty the return object is for anonymous access. Else returns an auth object that supports basic authentication.
 

Args :
        'username' : the username of the user.
        'password' : the password of the user.
Raises :
        ValueError in case one of the two arguments is empty.
 

>>> conn = HttpRequest('<transifex_host', auth = d)
>>> registry.setup({'http_handler': conn})
 

Creating a project
 

The model class for projects takes some arguments to successfully create a project. The mandatory fields are 'slug', 'name', 'owner', 'source_language'.
 

>>> from txlib.api.project import Project
 

>>> p = Project()
>>> p.slug = '<project_slug'>
>>> p.name = 'Project_name'
>>> p.description = 'This is a sample project'
>>> p.source_language_code = 'en'
>>> p.save()
 

Deleting a project
 

>>> from txlib.api.project import Project
 

>>> p = Project().get(slug='<project_slug>')
>>> p.delete()
 

Creating a resource
 

The model class for the resources takes some arguments and the mandatory fields are 'slug', 'name', 'mimetype' 
 

>>> from txlib.http.exceptions import *
>>> from txlib.api.resources import Resource
 

>>> try:
>>>  r = Resource().get(project_slug='<project_slug>', slug='<resource_slug>')
>>> exception NotFoundError:
>>>  r = Resource(project_slug='<project_slug>', slug='<resource_slug>')
>>>  r.name = 'Resource name'
>>>  r.i18n_type = 'PO'
>>> content = open(filename, 'r')
>>>  r.content = content.read()
>>>  content.close()
>>> r.save()
 

Creating or updating a translation
 

The model class for the translations. The only mandatory fields it has is the 'content' field.
 

>>> from txlib.api.translations import Translation
 

>>> t = Translation(project_slug = '<project_slug>', slug = '<resource_slug>', lang = 'el_GR')
>>> content = open(localized_filename,'r')
>>> t.content = content.read()
>>> content.close()
>>> t.save()
 

Downloading a translation
 

>>> from txlib.api.translations import Translation
 

>>> t = Translation(project_slug = '<project_slug>', slug = '<resource_slug>', lang = 'el_GR')
>>> trans = open(localized_filename,'w')
>>> strings = t.content
>>> trans.write(strings.encode('UTF-8'))
>>> trans.close()
 


