class Affiliation(object):
	def __init__(self, obj, t):
		self.supplierName = obj.get('supplierName', '')
		self.price        = obj.get('price', {'currency': 'USD', 'amount': 0})
		self.price['amount'] = float(self.price.get('amount', 0))
		self.buyLink      = obj.get('buyLink', '')
		self.supplierIcon = obj.get('supplierIcon', '')
		self.isSearch     = int(obj.get('isSearch', 0))
		self.type         = t
	