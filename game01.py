import mysql.connector
import random
from financesector import *


#--- Global Variables ---#

gcounter = 1; #global counter, perhaps for object id's
lottoticketlist = []
winning_numbers = []
Users = {}

acct_types = {1: 'CHQ', 2: 'CR', 3: 'GR', 4: 'LN', 5: 'BNK', 6: 'TRN'}
acct_t_longform = {1: 'CHEQUEING', 2: 'CREDIT', 3: 'GRANT', 4: 'LOAN', 5: 'BANK HOLDING', 6: 'TRANSFER'}

#--- Database Initialization ---#

db = mysql.connector.connect(
	host='localhost',
	user='root',
	passwd='!Osborne27',
	database='GAME01'
)

dbcursor = db.cursor()

'''
pr- property class
db- database

pid- property id, primary key in db
pclass_id- property class ID (so far, 1-4)
reg (CUR_REG in db)- current registrant of the property
value (PVAL in db)- current value of the property

'''

#--- Class definitions for property and money stuff ---#

class prop:
	def __init__(self, pid, pclass_id, registrant, value):
		self.pclass_id = pclass_id
		self.registrant = registrant
		self.value = value

class acct:
	def __init__(self, type_id, acn, registrant='BNK', comment = ''):
		
		self.type_id = type_id #INT, 1=CHQ 2=CR 3=GR 4=LN 5=BNK 6=Buffer
		self.acn = acn # VARCHAR 9 NOT NULL
		self.tokens = {}
		self.registrant = registrant
		self.comment = comment

	def addToken(self, token):
		self.tokens[token.token_id] = token #store token object in 'tokens' dict, with token_id as key
	
	def getBalance(self):
		return len(self.tokens)
	def remToken(self, token_dict, token_id=-1):
		if token_id == -1:
			temptoken = self.tokens.popitem()
			token_dict[temptoken[0]] = temptoken[1]
		elif token_id >= 0:
			temptoken = self.tokens.pop(token_id)
			token_dict[temptoken.token_id] = temptoken
		else:
			print ( "Token ID {} invalid.".format(token_id) )


def accountLookup(userid):
	user = userLookup(userid)
	accountnumlist = []
	if(user):
		for i in accounts:
			if accounts[i].registrant.user_id == userid:
				accountnumlist.append(i)
		return accountnumlist
	else:
		return 0




def newAccount(type_id, user_id, comment='', acn=False):
	acounter = '001'

	if (acn):
		if user_id in Users:
			accounts[acn] = acct (type_id, acn, Users[user_id], comment)
		else:
			print( 'User ID {} not available'.format(user_id) )
			return False
		
	elif user_id in Users:

		serial = Users[user_id].serial
		acn = str(serial) + '-0' + str(user_id) + '-' + acct_types[type_id] + acounter
		buffer = '00'
		while acn in accounts.keys():
			acounter = int(acounter) + 1
			if acounter < 10:
				buffer = '00'
			elif 999 >= acounter >= 10:
				buffer = '0'
			elif 9999 >= acounter >= 100:
				buffer = ''
			else:
				print ("Accounts per user of same type limited to 9999.")
				return -1

			acounter = buffer + str(acounter)
			acn = str(serial) + '-0' + str(user_id) + '-' + acct_types[type_id] + acounter

			

		accounts[acn] = acct (type_id, acn, Users[user_id], comment)

	else: print ("User Id Invalid")
			
	print( "Account Number:\t{}\t\tAccount Type:\t{}\t{}".format(accounts[acn].acn, acct_types[accounts[acn].type_id], acct_t_longform[accounts[acn].type_id]) )
	print( "Registrant:\t{}\t\t{}\t{}\t".format(accounts[acn].registrant.name, accounts[acn].registrant.user_sign, accounts[acn].registrant.user_id) )

def initialize_finance():
	initBank()
	genTokens(1, 10000000, 1, 'a00001')

def initBank():
	return;


class loan:
	def __init__(self, p, i, term, t_terms, b): #t_terms is time passed expressed in terms
		self.p, self.i, self.term, self.t_terms, self.b = p, i, term, t_terms, b

#--- Other Stuff ---#


class User:
	def __init__(self, user_id, user_sign, name, serial = 'C00'): #miscellaneaus registrations
		self.user_id = user_id
		self.user_sign = user_sign
		self.name = name
		self.assoc = ''

		self.serial = serial



#----- Lotto Section -----#

class lotto_ticket:
	
	def __init__(self, ticketNumbers, registrant, value, cost):
		self.ticketNumbers = ticketNumbers.copy()
		self.registrant = registrant
		self.value = value
		self.cost = cost
		# Validation Variables
		self.nmatch = 0 #number of matches
		self.alreadyMatched = []
		self.has_been_checked = False
	
	def checkTicket(self, wn, pl): #wn= winning number list, pl = prize amount list
		self.nmatch = 0 #initialize counter
		for i in range (0, 3):
			for x in range (2, -1, -1):
				if wn[i] == self.ticketNumbers[x] and self.ticketNumbers[x] not in self.alreadyMatched:
					self.nmatch += 1
					self.alreadyMatched.append( self.ticketNumbers[x] )
		self.value = pl[self.nmatch]
		self.alreadyMatched.clear()
		self.has_been_checked = True

def checkTicketLot(start=0, stop = -1, wn = winning_numbers, pl = [0, 10, 100, 9999], lot=lottoticketlist):
	if stop == -1:
		stop = len(lot)

	for i in range(start, stop):
		lot[i].checkTicket(wn, pl)


def ticketSummary(lot=lottoticketlist, showlosers=False):

	ctl = []
	btl = []
	atl = []
	ztl = []

	

	for i in range ( 0, len(lottoticketlist) ):
		if lottoticketlist[i].nmatch == 3:
			ctl.append(i)

		elif lottoticketlist[i].nmatch == 2:
			btl.append(i)

		elif lottoticketlist[i].nmatch == 1:
			atl.append(i)
		
		if showlosers == True:

			if lottoticketlist[i].nmatch == 0:
				ztl.append(i)
	if len(ctl) > 0:
		print("\n3 Winning Numbers:\nReg\tWinning Amnt\tMatches\tTicket #\n")
		for i in ctl:
			print( "{}\t{}\t\t{}\t{}".format(lottoticketlist[i].registrant, lottoticketlist[i].value, lottoticketlist[i].nmatch, i) )

	if len(btl) > 0:
		print("\n2 Winning Numbers:\nReg\tWinning Amnt\tMatches\tTicket #\n")
		for i in btl:
			print( "{}\t{}\t\t{}\t{}".format(lottoticketlist[i].registrant, lottoticketlist[i].value, lottoticketlist[i].nmatch, i) )

	if len(atl) > 0:
		print("\n1 Winning Number:\nReg\tWinning Amnt\tMatches\tTicket #\n")
		for i in atl:
			print( "{}\t{}\t\t{}\t{}".format(lottoticketlist[i].registrant, lottoticketlist[i].value, lottoticketlist[i].nmatch, i) )

	if len(ztl) > 0:
		print("\n0 Winning Numbers:\nReg\tWinning Amnt\tMatches\tTicket #\n")
		for i in ztl:
			print( "{}\t{}\t\t{}\t{}".format(lottoticketlist[i].registrant, lottoticketlist[i].value, lottoticketlist[i].nmatch, i) )




def gentickets(n):
	global lottoticketlist
	ticknums = []
	
	for i in range (1, n+1):
		
		for i in range (0, 3):
			ticknums.append( random.randrange(10) )
		
		lottoticketlist.append( lotto_ticket(ticknums, 'UNR', None, 100) )
		ticknums.clear()


def drawNums():
	global winning_numbers
	winning_numbers.clear()
	for i in range (0, 3):
		winning_numbers.append( random.randrange(10) )


def sellTicket(quant, baserate, freg='UNR', usign=0, uid=0):
	
	u = userLookup(uid, usign)
	c = 0
	buylist = []
	cost = 0
	userinput = 0

	if u == 0: #Check if user exists
		print("User could not be found.")
		return 0

	for i in range (0, len(lottoticketlist) ): #Make a list of tickets to buy
		if lottoticketlist[i].registrant == freg:
			c +=1
			buylist.append(i)
		if c == quant:
			break
	if c == 0:
		print("No lotto tickets are currently available from {}".format(freg))
	elif c < quant: #not enough tickets available
		userinput = (input("Only {} tickets are available from {}. Would you like to buy all {} tickets? (y/n)".format(c, freg, c))).lower()
		if userinput == 'y':
			sellTicket(c, baserate, freg, usign, uid) #recall function with quantity we know is available
		elif userinput == 'n':
			return 0
		else:
			print("Invalid input. Presuming 'n'")
			return 0

	else:
		cost = baserate * ( len(buylist) )
		userinput = (input("{} tickets will cost ${}. Confirm? (y/n) ".format(len(buylist), cost))).lower()
		if userinput == 'y':
			if ( tastyBird(u.user_id, 'lottosales', cost) ):
				for i in buylist:
					lottoticketlist[i].registrant = u.user_id
				print("Payment Successful.The following tickets have been purchased:\n\nTicket ID\tTicket Numbers")
				for i in buylist:
					print ( "{}\t{}\t{}\t{}".format(i, lottoticketlist[i].ticketNumbers[0], lottoticketlist[i].ticketNumbers[1], lottoticketlist[i].ticketNumbers[2]) )
				#payment successful; register each ticket in buylist to user
			else:
				print("Transaction Not Completed")
				return 0
				
		elif userinput == 'n':
			return 0
		else:
			print("Invalid input. Presuming 'n'")
			return 0 
	return 1;

def tastyBird(fromuserid, toaccount, amnt):
	print("\nWelcome to the TastyBird Payment Processor\n")
	user = userLookup(uid=fromuserid)
	usersign = 0
	username = 0
	fromaccount = 0

	if(user):
		usersign = user.user_sign
		username = user.name
		print ( "Summary of Accounts for User {} ({}): \n".format(username, fromuserid) )
		useraccounts = accountLookup(fromuserid) # accountLookup returns a list of account numbers belonging to fromuser
		print("N \tAccount Number\t\tBalance\t\tComment")
		for i in range(1, len(useraccounts)+1):
			runningaccount = accounts[useraccounts[i-1]]
			print ("{}.\t{}\t\t{}\t\t{}".format(i, useraccounts[i-1], runningaccount.getBalance(), runningaccount.comment))
		userinput = input("Select N of desired payment account: ")
		fromaccount = useraccounts[int(userinput)-1] # ***needs error handling ***
		#transfer money stuff
		if (input( "Confirm payment of {} to {} from {}?".format(amnt, accounts[toaccount].registrant.name, fromaccount) )).lower() == 'y':
			return fundsTransfer(toaccount, fromaccount, amnt)
		else:
			print("Payment Cancelled")
			return 0
	else:
		print("User {} does not exist".format(fromuserid))
		return 0



def fundsTransfer(inact, outact, amnt):
	inactorigin = len(accounts[inact].tokens)
	if inact in accounts and outact in accounts:
		if len(accounts[outact].tokens) >= amnt:
			for i in range(0, amnt):
				accounts[outact].remToken(accounts[inact].tokens)
		else:
			print ("Insufficient Funds")
			return 0
		print("{} tokens deposited.".format(len(accounts[inact].tokens)-inactorigin))
		return 1
	else:
		print ("One or both accounts do not exist.")
		return 0
			

def testingInit():

	Users[100] = User(100, 'TST', "Test User", 'T99')
	newAccount(1, 100)
	newAccount(1,100)
	newAccount(1, 100, acn='lottosales')

	genTokens(1, 1000, 1, 'T99-0100-CHQ001')

	print( "Acct 1 Balance: {}\n".format(accounts['T99-0100-CHQ001'].getBalance()) )
	print( "Acct 2 Balance: {}\n".format(accounts['T99-0100-CHQ002'].getBalance()) )


	gentickets(10)
	print("10 Tickets Generated.\n")

def testLotto():
	testingInit()
	sellTicket(5, 100, 'UNR', uid=100)
	drawNums()
	checkTicketLot()

def clearTickets(lot=lottoticketlist):
	lot.clear()

	

def userLookup(uid = 0, usign = 0, uname = 0):	#not case sensitive
	if (uid):
		if uid in Users:
			return Users[uid]	#Fastest
		else: return 0
	elif (usign):
		for i in Users:
			if Users[i].user_sign.lower() == usign.lower():
				return Users[i]
		return 0
	elif (uname):
		for i in Users:
			if uname.lower() == Users[i].name.lower():
				return Users[i]
		return 0
	else: print("User lookup service requires one of user id (uid), user sign (usign), or user name (uname) to be provided.")

