from dateutil import parser

class Image(object):
	def dict(self):
		'''Returns a dictionary representation of self. This is
		particularly useful if, say, you want to JSON-encode this'''
		
		# These are all the attributes that are primitives already
		atts = ('title', 'url', 'dateadded', 'format', 'size')
		return dict((key, self.__getattribute__(key)) for key in atts)
	
	def __init__(self, obj):
		self.title     = obj.get('title', '')
		self.url       = obj.get('url', '')
		self.dateadded = parser.parse(obj.get('dateadded', ''))
		self.format    = obj.get('format', '')
		self.sizes     = obj.get('sizes', {}).get('size', [])
		self.sizes     = dict((s.get('name', ''), {
			'url': s.get('#text', ''),
			'width': int(s.get('width', 0)),
			'height': int(s.get('height', 0))
		}) for s in self.sizes)
	