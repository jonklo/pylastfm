#!/usr/bin/env python
"""Encapsulates interactions with Last.FM."""

import urllib                           # For parsing urls
import urllib2                          # For loading urls
import simplejson as json               # For parsing results

__author__     = "Dan Lecocq"
__copyright__  = "Copyright 2011, Ingenious Designs Inc."
__credits__    = ["Dan Lecocq"]
__license__    = "TBD"
__version__    = "0.1"
__maintainer__ = "Dan Lecocq"
__email__      = "dan.lecocq@kaust.edu.sa"
__status__     = "Development"
                                                  
base = "http://ws.audioscrobbler.com/2.0/?method=%s&%s&api_key=b25b959554ed76058ac220b7b2e0a026&format=json"

class LastError(Exception):
	"""The exception raised when a query fails"""
	def __init__(self, value):
		self.value = value
	def __repr__(self):
		return repr(self.value)
	def __str__(self):
		return str(self.value)

def lasterror(fn):
	'''Wrap the method in a try/except block that raises a LastError'''
	def wrapped(*args, **kwargs):
		try:
			return fn(*args, **kwargs)
		except Exception as e:
			raise LastError(e)
	return wrapped

def query(method, params):
	"""Send a request command with params to Last.FM API"""
	try:
		for k, v in params.items():
			if isinstance(v, unicode):
				params[k] = v.encode('utf-8')
		return json.loads(urllib2.urlopen(base % (method, urllib.urlencode(params))).read())
	except Exception as e:
		print repr(e)
		raise LastError("LastFM query error.")

from affiliation import Affiliation
from artist import Artist
from album import Album
from event import Event
from image import Image
from track import Track
from venue import Venue
from tag import Tag