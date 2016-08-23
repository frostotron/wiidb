#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name = 'wiidb',
    version = '0.2',
    author = 'frostotron',
    author_email = 'frostotron@post.com',
    description = 'A Python library for downloading and processing wiitdb.zip from gametdb.com',
    license = 'GPL3',
    packages = ['wiidb', 'tests'],
    install_requires = ['urllib3']
)
