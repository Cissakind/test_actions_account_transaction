class transaction:
	def __init__(self, merchant, transaction_time, transaction_amount):
		self.merchant = merchant
		self.transaction_time = transaction_time
		self.transaction_amount = transaction_amount

class account:
	def __init__(self, active, availableLimit):
		self.active = active
		self.availableLimit = availableLimit
		self.newAccount = True
		self.history = []

	def isAccountActive(self):
		return self.active

	def first_transaction_above_threshold(self, transaction_value):
		if self.newAccount:
			if transaction_value > self.availableLimit*0.9:
				return True
		return False

	def insufficient_limit(self, transaction_value):
		return (transaction_value >  self.availableLimit)

	def doubled_transaction(self, newTransaction):
		transaction_size = len(self.history)

		if transaction_size >= 1:
			for transaction in self.history:
				if (newTransaction.merchant == transaction.merchant and
				    newTransaction.transaction_time - transaction.transaction_time < 120):
					return True
		return False

	def high_frequency_small_interval(self, newTransaction):
		transaction_size = len(self.history)

		if(transaction_size >= 2):
			return ( newTransaction.transaction_time - self.history[transaction_size - 2].transaction_time) < 180

		return False


	def updateBalance(self, transaction_value):
		self.availableLimit = self.availableLimit - transaction_value

	def addTransaction(self, newTransaction):
		self.newAccount = False
		self.history += [newTransaction]


def autorizador(newTransaction, account):
	violations = []
	resultAccount = None

	if(not account.isAccountActive()):
	
		resultAccount = account
		violations += ["account-not-active"]
		return resultAccount, violations
	

	elif (account.first_transaction_above_threshold(newTransaction.transaction_amount)):	
		
		resultAccount = account;
		violations += ["first-transaction-above-threshold"]
		return resultAccount, violations
	

	elif (account.insufficient_limit(newTransaction.transaction_amount)):
	
		resultAccount = account;
		violations += ["insufficient-limit"]
		return resultAccount, violations
	

	elif (account.high_frequency_small_interval(newTransaction)):
	
		resultAccount = account;
		violations += ["high_frequency_small_interval"]
		return resultAccount, violations
	

	elif (account.doubled_transaction(newTransaction)):
	
		resultAccount = account;
		violations += ["doubled-transaction"]
		return resultAccount, violations
	

	account.updateBalance(newTransaction.transaction_amount)
	account.addTransaction(newTransaction)
	resultAccount = account
	return resultAccount, violations

