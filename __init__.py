#!/usr/bin/env python
"""Encapsulates interactions with Last.FM."""

import re                               # For cleaning up similar artists
import urllib                           # For parsing urls
import urllib2                          # For loading urls
import difflib
import sphinxapi
import threading                        # For extended queries
import simplejson as json               # For parsing results
from collections import deque           # Queuing up elements to explore

__author__     = "Dan Lecocq"
__copyright__  = "Copyright 2011, Ingenious Designs Inc."
__credits__    = ["Dan Lecocq"]
__license__    = "TBD"
__version__    = "0.1"
__maintainer__ = "Dan Lecocq"
__email__      = "dan.lecocq@kaust.edu.sa"
__status__     = "Development"
                                                  
base = "http://ws.audioscrobbler.com/2.0/?method=%s&%s&api_key=b25b959554ed76058ac220b7b2e0a026&format=json"
# &autocorrect=1

class LastError(Exception):
	"""The exception raised when a query fails"""
	def __init__(self, value):
		self.value = value
	def __repr__(self):
		return repr(self.value)
	def __str__(self):
		return str(self.value)

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

def cleanTitles(artist, videos):
	try:
		# For stripping out the artist's name from titles
		reName = re.compile(r'(\W+|^)%s(\W+|$)' % artist.lower(), re.I)
		titles = [t['name'] for t in Artist.getTopTracks(artist, 200)]
		# Strip out everything in () or []
		titles = [re.sub(r'(\W+|^)\([^\(\)]+\)(\W+|$)', '', t) for t in titles]
		titles = [re.sub(r'(\W+|^)\([^\(\)]+\)(\W+|$)', '', t) for t in titles]
		titles = [re.sub(r'(\W+|^)\[[^\[\]]+\](\W+|$)', '', t) for t in titles]
		titles = [re.sub(r'(\W+|^)\[[^\[\]]+\](\W+|$)', '', t) for t in titles]
		# Remove the artist's name from titles
		titles = [reName.sub('', t) for t in titles]
		# Remove leading and trailing non-chars
		titles = [re.sub(r'^\W+|\W+$', '', t) for t in titles]
		# Make them unique at least by key
		titles = dict([(re.sub(r'\W+', '', t.lower()), t) for t in titles]).values()
		# Build up all our regular expressions
		regs = [re.sub(r'\W+', '.*', t.lower()) for t in titles]
		regs = [re.compile(r'(\W|^)%s(\W|$)' % r, re.I) for r in regs]
		regs = dict([(regs[i], titles[i]) for i in range(len(regs)) if (not regs[i].search(artist))])
		
		# Clean out titles that are matched by other titles
		out = {}
		for reg, title in regs.items():
			found = False
			for other in regs:
				if (other != reg) and other.search(title):
					print '%s matched %s' % (title, regs[other])
					found = True
			if not found:
				out[reg] = title
		regs = out

		success = 0
		for video in videos:
			matches = []
			for reg in regs:
				if reg.search(video['title']):
					matches.append(regs[reg])
			if len(matches) == 1:
				video['cleaned'] = matches[0]
				success += 1
			else:
				matches = difflib.get_close_matches(video['title'], matches, 1, 0.3)
				if len(matches):
					video['cleaned'] = matches[0]
					success += 1
				else:
					video['cleaned'] = repr(None)
	except LastError:
		for video in videos:
			video['cleaned'] = video['title']
	return videos

class Artist(dict):
	"""Methods related to artists, as well as an artist object."""
	@staticmethod
	def getInfo(artist):
		"""Call Last.FM's artist.getInfo method."""
		try:
			return Artist(search("artist.getinfo", {"artist":artist})["artist"])
		except (KeyError, TypeError):
			raise LastError("Couldn't get artist info for %s" % artist)
	
	@staticmethod
	def getAlbums(artist, count=20):
		"""Call Last.FM's artist.topAblums method."""
		try:
			albums = search("artist.topAlbums", {"artist":artist, "limit":count})["topalbums"]["album"]
			r = re.compile(r'%s' % re.sub(r'\W+', '.*', artist), re.I)
			return [album for album in albums if r.search(album['artist']['name'])]
		except (KeyError, TypeError):
			raise LastError("Couldn't get albums for artist %s" % artist)
	
	@staticmethod
	def getTopTracks(artist, count=100):
		"""Call Last.FM's artist.topTracks method."""
		try:
			tracks = search("artist.topTracks", {"artist":artist, "limit":count})["toptracks"]["track"]
			return tracks
		except (KeyError, TypeError):
			raise LastError("Couldn't get top tracks for %s" % artist)
	
	@staticmethod
	def getImages(artist, count=10):
		"""Get the images for a given artist from Last.FM"""
		try:
		 	images = search("artist.getImages", {"artist":artist, "limit":count})["images"]["image"]
			results = []
			for img in images:
				try:
					sizes = dict([(i['width'], i['#text']) for i in img['sizes']['size']])
					results.append(sizes['126'].split('/')[-1])
				except (KeyError, IndexError, TypeError):
					continue
			return results
		except (KeyError, TypeError):
			raise LastError("Couldn't get images for %s" % artist)
	
	@staticmethod
	def filter(name, artists):
		"""Filter out artists from the list of artist based on name."""
		# Filter out artists if:
		# 1) Their name is too similar to this artist
		# 2) Their name contains ft., feat., etc.
		# 3) Their name contains vs., versus.
		# 4) Their name contains pres.
		# 5) Their name contains "/"
		reName = re.sub(r'\W+', '.*', name)
		nameTest = re.compile("(\W|^)(%s|f(ea)?t\.?|featuring|v(ersus)?s\.?|\/|\,|with|www|https?|com|org|net|us|cc|info)(\W|$)" % reName, re.I)
		return [{'name':a['name'], 'img':a['img']} for a in artists if (not nameTest.search(a['name']))]
		
	def __init__(self, data):
		"""Build an artist object with Last.FM-formatted artist data."""
		self['name'     ] = getDefault(data, lambda o: o['name'], '')
		self['mbid'     ] = getDefault(data, lambda o: o['mbid'], '')
		self['listeners'] = getDefault(data, lambda o: int(o['listeners']), 0)
		self['playcount'] = getDefault(data, lambda o: int(o['playcount']), 0)
		self['listeners'] = getDefault(data, lambda o: int(o['stats']['listeners']), self['listeners'])
		self['playcount'] = getDefault(data, lambda o: int(o['stats']['playcount']), self['playcount'])
		self['img'      ] = getDefault(data, lambda o: o['image'][0]['#text'].split('/')[-1], '')
		self['bio'      ] = getDefault(data, lambda o: o['bio']['summary'], '')
		self['bio'      ] = re.sub(r'\<(\w+).+?\>(.+?)\<[^\>]+?\1\>', lambda m: m.group(2), self['bio'])
		self['similar'  ] = getDefault(data, lambda o: [Artist(a) for a in o['similar']['artist']], [])
		self['tags'     ] = getDefault(data, lambda o: [t['name'] for t in o['tags']['tag']], [])
		self['images'   ] = []
	
	def __setitem__(self, name, value):
		"""Always ensures the setting similar artists passes through the filter."""
		if (name == 'similar'):
			return dict.__setitem__(self, 'similar', Artist.filter(self['name'], value))
		else:
			return dict.__setitem__(self, name, value)

class Album:
	"""Methods related to Last.FM's album methods."""
	@staticmethod
	def tracks(artist, album, count=20):
		"""Get all the tracks from an album"""
		try:
			tracks = search("album.getInfo", {"artist":artist, "album":album, "limit":count})["album"]["tracks"]["track"]
			if (isinstance(tracks, dict)):
				return [tracks]
			else:
				return tracks
		except (KeyError, TypeError):
			raise LastError("Couldn't get tracks for album %s by %s" % (artist, album))

class Tag:
	"""Methods related to Last.FM's tag methods."""
	@staticmethod
	def topArtists(tag, count=10):
		"""Get the top artists for any given tag."""
		try:
			return [Artist(a) for a in search("tag.gettopartists", {"tag":tag, "limit":count})["topartists"]["artist"]]
		except KeyError:
			raise LastError("Couldn't get top artists for '%s'" % tag)
	
	@staticmethod
	def topTags(count=100):
		"""Get the top tags on Last.FM"""
		try:
			return search("tag.getTopTags", {})["toptags"]["tag"][0:count]
		except KeyError:
			raise LastError("Couldn't get top tags.")

class Chart:
	"""Last.FM Chart methods"""
	@staticmethod
	def topArtists(count=100):
		"""Get the current top artists."""
		try:
			return [Artist(a) for a in search("chart.getTopArtists", {"limit":count})["artists"]["artist"]]
		except KeyError:
			raise LastError("Couldn't get chart's topArtists")