#!/usr/bin/env python

from setuptools import setup, find_packages

install_requires = []
try:
    import json
except ImportError:
    install_requires.append('simplejson')

try:
    import unittest2
except ImportError:
    install_requires.append('unittest2')

setup(
    name="txlib",
    author="Indifex Ltd.",
    author_email="info@indifex.com",
    description="A python library for Transifex",
    url="http://www.indifex.com",

    packages=find_packages(),
    install_requires = install_requires,

    keywords = (
        'translation',
        'localization',
        'internationalization',
    ),
    license='LGPL3',
)
