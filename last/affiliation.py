class Affiliation(object):
	def dict(self):
		'''Returns a dictionary representation of self. This is
		particularly useful if, say, you want to JSON-encode this'''
		
		# These are all the attributes that are primitives already
		atts = ('supplierName', 'price', 'buyLink', 'supplierIcon', 'isSearch', 'type')
		return dict((key, self.__getattribute__(key)) for key in atts)
	
	def __init__(self, obj, t):
		self.supplierName = obj.get('supplierName', '')
		self.price        = obj.get('price', {'currency': 'USD', 'amount': 0})
		self.price['amount'] = float(self.price.get('amount', 0))
		self.buyLink      = obj.get('buyLink', '')
		self.supplierIcon = obj.get('supplierIcon', '')
		self.isSearch     = int(obj.get('isSearch', 0))
		self.type         = t
	