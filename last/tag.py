from last import query

class TagResults(object):
	def __init__(self, obj):
		self.searchTerms  = obj.get('opensearch:Query', {}).get('searchTerms', '')
		self.totalResults = int(obj.get('opensearch:totalResults', 0))
		self.itemsPerPage = int(obj.get('opensearch:itemsPerPage', 30))
		self.artists = [Artist(a) for a in obj.get('artistmatches', {}).get('artist', [])]
		
class Tag(object):
	def dict(self):
		'''Returns a dictionary representation of self. This is
		particularly useful if, say, you want to JSON-encode this'''
		
		# These are all the attributes that are primitives already
		atts = ('name', 'count', 'url')
		return dict((key, self.__getattribute__(key)) for key in atts)
	
	def __init__(self, obj):
		'''Initialize an event based on the provided dictionary'''
		self.name  = obj.get('name', '')
		self.count = int(obj.get('count', 0))
		self.url   = obj.get('url', '')
