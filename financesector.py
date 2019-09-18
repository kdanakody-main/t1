
accounts = {}
fullSum = [] #list in which to store balances as they're added so that sum of all balances can be calculated

class token:
	def __init__(self, token_id, value = 1):
		self.token_id = token_id
		self.value = value

	

def genTokens(start_id, n, value, acn):
	if acn in accounts:
		for i in range (start_id, n+1):
			accounts[acn].addToken( token(i, value) )
	else: print ("Account {} does not exist.".format(acn))






