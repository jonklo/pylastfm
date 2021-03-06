from last import query
from last import lasterror

class TrackResults(object):
	def __init__(self, obj):
		self.searchTerms  = obj.get('opensearch:Query', {}).get('searchTerms', '')
		self.totalResults = int(obj.get('opensearch:totalResults', 0))
		self.itemsPerPage = int(obj.get('opensearch:itemsPerPage', 30))
		self.artists = [Track(t) for t in obj.get('trackmatches', {}).get('track', [])]
		
class Track(object):
	'''Represents a Last.FM track'''
	@staticmethod
	@lasterror
	def search(track, artist=None, page=1, limit=30):
		'''Search for tracks by the provided name'''
		params = {'track': track, 'page':page, 'limit': limit}
		if artist:
			params['artist'] = artist
		return TrackResults(query('track.search', params).get('results', {}))
	
	def dict(self):
		'''Returns a dictionary representation of self. This is
		particularly useful if, say, you want to JSON-encode this'''

		# These are all the attributes that are primitives already
		atts = ('name', 'listeners', 'playcount', 'mbid', 'url', 'match', 'images')
		return dict((key, self.__getattribute__(key)) for key in atts)
	
	def __init__(self, obj):
		'''Initialize an artist based on the provided dictionary'''
		self.name       = obj.get('name', '')
		self.listeners  = int(obj.get('listeners', 1))
		self.playcount  = int(obj.get('playcount', 1))
		self.mbid       = obj.get('mbid', None)
		self.url        = obj.get('url', None)
		self.match      = float(obj.get('match', 0))
		self.images     = {}
		for i in obj.get('image', []):
			self.images[i.get('size', 'small')] = i.get('#text', None)
	