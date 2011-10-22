from dateutil import parser

class Image(object):
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
	