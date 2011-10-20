from last import query
from last import LastError

class AlbumResults(object):
	def __init__(self, obj):
		self.searchTerms  = obj.get('opensearch:Query', {}).get('searchTerms', '')
		self.totalResults = int(obj.get('opensearch:totalResults', 0))
		self.itemsPerPage = int(obj.get('opensearch:itemsPerPage', 30))
		self.artists = [Artist(a) for a in obj.get('artistmatches', {}).get('artist', [])]
		
class Album(object):
	'''Represents a Last.FM ablum'''
	@staticmethod
	def search(artist, page=1, limit=50):
		'''Search for artists by the provided name'''
		return ArtistResults(query('artist.search', {'artist': artist, 'page':page, 'limit': limit}).get('results', {}))
	
	def __init__(self, obj):
		'''Initialize an artist based on the provided dictionary'''
		self.name       = obj.get('name', '')
		self.playcount  = int(obj.get('playcount', 1))
		self.mbid       = obj.get('mbid', None)
		self.url        = obj.get('url', None)
		self.match      = float(obj.get('match', 0))
		self.artist     = Artist(obj.get('artist', {}))
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
