from last import query
from last import lasterror
from last.tag import Tag
from last.album import Album
from last.track import Track
from last.event import Event
from last.image import Image

class ArtistResults(object):
	def __init__(self, obj):
		self.searchTerms  = obj.get('opensearch:Query', {}).get('searchTerms', '')
		self.totalResults = int(obj.get('opensearch:totalResults', 0))
		self.itemsPerPage = int(obj.get('opensearch:itemsPerPage', 30))
		self.artists = [Artist(a) for a in obj.get('artistmatches', {}).get('artist', [])]
		
class Artist(object):
	'''Represents a Last.FM artist'''
	@lasterror
	@staticmethod
	def search(artist, limit=50, page=1):
		'''Search for artists by the provided name'''
		return ArtistResults(query('artist.search', {'artist': artist, 'page':page, 'limit': limit}).get('results', {}))
	
	@lasterror
	@staticmethod
	def getCorrection(artist):
		'''Get the name correction for the provided artist'''
		result = query('artist.getcorrection', {'artist': artist})
		return [Artist(a.get('artist', {})) for a in result.get('corrections', {}).get('correction', []) if isinstance(a)]
	
	@lasterror
	@staticmethod
	def getEvents(artist, limit=50, page=1, autocorrect=1, festivalsonly=0):
		result = query('artist.getevents', {'artist':artist, 'autocorrect':1, 'limit':limit, 'page':page, 'festivalsonly':festivalsonly})
		return [Event(e) for e in result.get('events', {}).get('event', []) if isinstance(e)]
	
	@lasterror
	@staticmethod
	def getImages(artist, limit=50, page=1, autocorrect=1, order='popularity'):
		result = query('artist.getimages', {'artist':artist, 'limit':limit, 'page':page, 'autocorrect':autocorrect, 'order':order})
		return [Image(i) for i in result.get('images', {}).get('image', []) if isinstance(i)]
	
	@lasterror
	@staticmethod
	def getInfo(artist, autocorrect=1):
		raise Exception('Unimplemented.')
	
	@lasterror
	@staticmethod
	def getPastEvents(artist, limit=50, page=1, autocorrect=1):
		raise Exception('Unimplemented.')
	
	@lasterror
	@staticmethod
	def getPodcast(artist, autocorrect=1):
		raise Exception('Unimplemented.')
	
	@lasterror
	@staticmethod
	def getShouts(artist, limit=50, page=1, autocorrect=1):
		raise Exception('Unimplemented.')
	
	@lasterror
	@staticmethod
	def getSimilar(artist, limit=50, autocorrect=1):
		result = query('artist.getsimilar', {'artist':artist, 'limit':limit, 'autocorrect':autocorrect})
		return [Artist(e) for e in result.get('similarartists', {}).get('artist', []) if isinstance(e, dict)]
	
	@lasterror
	@staticmethod
	def getTopAlbums(artist, limit=50, page=1, autocorrect=1):
		result = query('artist.gettopalbums', {'artist':artist, 'limit':limit, 'page':page, 'autocorrect':autocorrect})
		return [Album(a) for a in result.get('topalbums', {}).get('album', []) if isinstance(a, dict)]
	
	@lasterror
	@staticmethod
	def getTopFans(artist, autocorrect=1):
		raise Exception('Unimplemented.')
	
	@lasterror
	@staticmethod
	def getTopTags(artist, autocorrect=1):
		result = query('artist.gettoptags', {'artist':artist, 'autocorrect':autocorrect})
		return [Tag(t) for t in result.get('toptags', {}).get('tag', []) if isinstance(t, dict)]
	
	@lasterror
	@staticmethod
	def getTopTracks(artist, limit=50, page=1, autocorrect=1):
		result = query('artist.gettoptracks', {'artist': artist, 'limit': limit, 'page': page, 'autocorrect': autocorrect})
		return [Track(t) for t in result.get('toptracks', {}).get('track', []) if isinstance(t, dict)]
	
	@lasterror
	@staticmethod
	def top(limit=50, page=1):
		result = query('chart.gettopartists', {'limit':limit, 'page':page})
		return [Artist(a) for a in result.get('artists', {}).get('artist', []) if isinstance(a)]
	
	@lasterror
	@staticmethod
	def get(artist, autocorrect=1, lang='en'):
		result = query('artist.getinfo', {'artist':artist, 'autocorrect':autocorrect, 'lang':lang})
		return Artist(result.get('artist', {}))
	
	def __init__(self, obj):
		'''Initialize an artist based on the provided dictionary'''
		self.name       = obj.get('name', '')
		stats           = obj.get('stats', None)
		if stats:
			# Sometimes parsing an int doesn't work out like you'd hope
			try:
				self.listeners = int(stats.get('listeners', 0))
			except:
				self.listeners = 0
			try:
				self.playcount = int(stats.get('playcount', 0))
			except:
				self.playcount = 0
		else:
			try:
				self.listeners = int(obj.get('listeners', 0))
			except:
				self.listeners = 0
			try:
				self.playcount = int(obj.get('playcount', 0))
			except:
				self.playcount = 0
		self.mbid       = obj.get('mbid', None)
		self.url        = obj.get('url', None)
		try:
			self.streamable = bool(obj.get('streamable', False))
		except:
			self.streamable = False
		try:
			self.match      = float(obj.get('match', 0))
		except:
			self.match      = 0
		self.bio        = obj.get('bio', {})
		self.images     = {}
		for i in obj.get('image', []):
			self.images[i.get('size', 'small')] = i.get('#text', None)
	
	def __getattr__(self, name):
		if name == 'similar':
			self.similar = Artist.getSimilar(self.name)
			return self.similar
		elif name == 'tracks':
			self.tracks = Artist.getTopTracks(self.name)
			return self.tracks
		elif name == 'events':
			self.events = Artist.getEvents(self.name)
			return self.events
		elif name == 'albums':
			self.albums = Artist.getTopAlbums(self.name)
			return self.albums
		elif name == 'images':
			self.images = Artist.getImages(self.name)
			return self.images
	
	def __getstate__(self):
		return self.__dict__
	
	def __setstate__(self, d):
		self.__dict__.update(d)