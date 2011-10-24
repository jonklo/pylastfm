from last import query
from last import LastError
from last.venue import Venue
from dateutil import parser

class EventResults(object):
	def __init__(self, obj):
		self.searchTerms  = obj.get('opensearch:Query', {}).get('searchTerms', '')
		self.totalResults = int(obj.get('opensearch:totalResults', 0))
		self.itemsPerPage = int(obj.get('opensearch:itemsPerPage', 30))
		self.artists = [Artist(a) for a in obj.get('artistmatches', {}).get('artist', [])]
		
class Event(object):
	def __init__(self, obj):
		'''Initialize an event based on the provided dictionary'''
		self.id          = obj.get('id', '')
		self.title       = obj.get('title', '')
		self.artists     = obj.get('artists', {}).get('artist', [])
		# Make sure this is an array
		if isinstance(self.artists, basestring):
			self.artists = [self.artists]
		self.headliner   = obj.get('artists', {}).get('headliner', '')
		self.venue       = Venue(obj.get('venue', {}))
		# Parse out the date
		self.startDate   = parser.parse(obj.get('startDate', ''))
		self.description = obj.get('description', '')
		# Get out the associated images
		self.images     = {}
		for i in obj.get('image', []):
			self.images[i.get('size', 'small')] = i.get('#text', None)
		# Get the attendance and reviews, whatever that means
		self.attendance = int(obj.get('attendance', 0))
		self.reviews    = int(obj.get('reviews', 0))
		self.tag        = obj.get('tag', '')
		self.url        = obj.get('url', '')
		self.website    = obj.get('website', '')
		self.tickets    = obj.get('tickets', '')
		self.cancelled  = int(obj.get('cancelled', 0))
		self.tags       = obj.get('tags', {}).get('tag', [])
	