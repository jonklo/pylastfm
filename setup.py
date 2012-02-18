#!/usr/bin/env python

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

setup(name = 'last',
	version = '0.2',
	description = 'Last.FM API interface',
	long_description = 'A Pythonic interface to the Last.FM API',
	author = 'Dan Lecocq',
	author_email = 'dan@lecocq.us',
	url = 'http://github.com/ingeniousdesigns/last',
	packages = ['last'],
	platforms = 'Posix; MacOS X; Windows',
	classifiers = []
)
