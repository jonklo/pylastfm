from last import query

class TagResults(object):
	def __init__(self, obj):
		self.searchTerms  = obj.get('opensearch:Query', {}).get('searchTerms', '')
		self.totalResults = int(obj.get('opensearch:totalResults', 0))
		self.itemsPerPage = int(obj.get('opensearch:itemsPerPage', 30))
		self.artists = [Artist(a) for a in obj.get('artistmatches', {}).get('artist', [])]
		
class Tag(object):
	def __init__(self, obj):
		'''Initialize an event based on the provided dictionary'''
		self.name  = obj.get('name', '')
		self.count = int(obj.get('count', 0))
		self.url   = obj.get('url', '')
