from last import query
from last import LastError

class VenueResults(object):
	def __init__(self, obj):
		self.searchTerms  = obj.get('opensearch:Query', {}).get('searchTerms', '')
		self.totalResults = int(obj.get('opensearch:totalResults', 0))
		self.itemsPerPage = int(obj.get('opensearch:itemsPerPage', 30))
		self.artists = [Artist(a) for a in obj.get('artistmatches', {}).get('artist', [])]
		
class Venue(object):
	def __init__(self, obj):
		'''Initialize an event based on the provided dictionary'''
		self.id          = obj.get('id', '')
		self.name        = obj.get('name', '')
		# Build up the location
		location         = obj.get('location', {}).get('geo:point')
		lat = float(location.get('geo:lat', 0))
		lon = float(location.get('geo:long', 0))
		self.location    = {'latitude': lat, 'longitude': lon}
		# Get the city, state, etc.
		self.city        = location.get('city', '')
		self.country     = location.get('country', '')
		self.street      = location.get('street', '')
		self.postalcode  = location.get('postalcode', '')
		# Get the remaining atts
		self.url         = obj.get('url', '')
		self.website     = obj.get('website', '')
		self.phonenumber = obj.get('phonenumber', '')
		# Get out the associated images
		self.images     = {}
		for i in obj.get('image', []):
			self.images[i.get('size', 'small')] = i.get('#text', None)		
