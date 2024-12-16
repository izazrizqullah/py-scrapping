#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: broono


import codecs
import os

try:
    from setuptools import setup, find_packages # type: ignore
except:
    from distutils.core import setup, find_packages # type: ignore


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


NAME = "alibabaa"
PACKAGES = find_packages()
REQUIREMENTS = ["requests", "bs4", "autouseragents", "self", "freexici"]
DESCRIPTION = "A non-official tool to fetch API like search results data from https://s.1688.com"
LONG_DESCRIPTION = read("README.rst")
KEYWORDS = "alibaba ali 1688 alimama"
AUTHOR = "Broono"
AUTHOR_EMAIL = "tosven.broono@gmail.com"
URL = "https://github.com/brunobell/alibabaa"
VERSION = "0.1.3"
LICENSE = "MIT"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    platforms=['any'],
    include_package_data=False,
    zip_safe=True,
    install_requires=REQUIREMENTS,
)
