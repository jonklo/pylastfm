from last import query
from last import LastError
from last.album import Album
from last.track import Track

class ArtistResults(object):
	def __init__(self, obj):
		self.searchTerms  = obj.get('opensearch:Query', {}).get('searchTerms', '')
		self.totalResults = int(obj.get('opensearch:totalResults', 0))
		self.itemsPerPage = int(obj.get('opensearch:itemsPerPage', 30))
		self.artists = [Artist(a) for a in obj.get('artistmatches', {}).get('artist', [])]
		
class Artist(object):
	'''Represents a Last.FM artist'''
	@staticmethod
	def search(artist, page=1, limit=50):
		'''Search for artists by the provided name'''
		return ArtistResults(query('artist.search', {'artist': artist, 'page':page, 'limit': limit}).get('results', {}))
	
	@staticmethod
	def getSimilar(artist, limit=50, autocorrect=1):
		result = query('artist.getsimilar', {'artist': artist, 'limit': limit, 'autocorrect': autocorrect})
		return [Artist(a) for a in result.get('similarartists', {}).get('artist', [])]
	
	@staticmethod
	def getTopAlbums(artist, limit=50, page=1, autocorrect=1):
		result = query('artist.gettopalbums', {'artist':artist, 'limit':limit, 'page':page, 'autocorrect':autocorrect})
		return [Album(a) for a in result.get('topalbums', {}).get('album', [])]
	
	@staticmethod
	def getTopTracks(artist, limit=50, page=1, autocorrect=1):
		result = query('artist.gettoptracks', {'artist': artist, 'limit': limit, 'page': page, 'autocorrect': autocorrect})
		return [Track(t) for t in result.get('toptracks', {}).get('track', [])]
	
	def __init__(self, obj):
		'''Initialize an artist based on the provided dictionary'''
		self.name       = obj.get('name', '')
		self.listeners  = int(obj.get('listeners', 1))
		self.mbid       = obj.get('mbid', None)
		self.url        = obj.get('url', None)
		self.streamable = bool(obj.get('streamable', False))
		self.match      = float(obj.get('match', 0))
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
	