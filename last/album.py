from last import query
from last import LastError
from last.tag import Tag
from last.affiliation import Affiliation

class AlbumResults(object):
	def __init__(self, obj):
		self.searchTerms  = obj.get('opensearch:Query', {}).get('searchTerms', '')
		self.totalResults = int(obj.get('opensearch:totalResults', 0))
		self.itemsPerPage = int(obj.get('opensearch:itemsPerPage', 30))
		self.albums = [Album(a) for a in obj.get('albummatches', {}).get('album', [])]
		
class Album(object):
	'''Represents a Last.FM ablum'''
	@staticmethod
	def search(album, limit=50, page=1):
		return AlbumResults(query('album.search', {'album':album, 'page':page, 'limit': limit}).get('results', {}))
	
	@staticmethod
	def getBuyLinks(artist, album, autocorrect=1, country='united states'):
		result = query('album.getbuylinks', {'artist': artist, 'album':album, 'autocorrect':autocorrect, 'country':country})
		affiliations = []
		for k, v in result.get('affiliations', {}).items():
			affiliations.extend([Affiliation(a, k) for a in v])
		return affiliations
	
	@staticmethod
	def getShouts(artist, limit=50, page=1, autocorrect=1):
		raise Exception('Unimplemented.')
	
	@staticmethod
	def getTopTags(artist, album, autocorrect=1):
		result = query('album.gettoptags', {'artist':artist, 'album':album, 'autocorrect':autocorrect})
		return [Tag(t) for t in result.get('toptags', {}).get('tag', [])]
	
	def __init__(self, obj):
		'''Initialize an artist based on the provided dictionary'''
		self.name       = obj.get('name', '')
		self.playcount  = int(obj.get('playcount', 1))
		self.mbid       = obj.get('mbid', None)
		self.url        = obj.get('url', None)
		self.match      = float(obj.get('match', 0))
		self.artist     = obj.get('artist', '')
		self.images     = {}
		for i in obj.get('image', []):
			self.images[i.get('size', 'small')] = i.get('#text', None)
	
	def __getattr__(self, name):
		if name == 'buylinks':
			self.buylinks = Album.getBuyLinks(self.artist, self.name)
			return self.buylinks
		elif name == 'tags':
			self.tags = Album.getTopTags(self.artist, self.name)
			return self.tags
	