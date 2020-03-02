userId = 0
amountAtHand  = 50000
accountNumber = 0
pin = 0
name = ''
mainArray = []
accountNotPresent = False

isLoggedIn = False
loggedInUser = {}
def registration():
	global name
	name = input('Input your name')
	print('name has been saved')
	numberAndPin()
def numberAndPin():
		global accountNumber, pin, amountAtHand, name
		try:
			accountNumber = int(input('Type your account Number'))
		except:
			notANumber()
		else:
			checkInArray()
			if accountNotPresent:
				print('account number has been saved')
			else:
				print('account number already exists')
				numberAndPin()
				return
			try:
				pin = int(input('Input your preferred pin'))
			except:
				notANumber()
			else:
				print('pin saved successfully')
				newUser = {'name': name, 'accountNumber': accountNumber, 'pin': pin, 
				'amountAtHand': amountAtHand}
				mainArray.append(newUser)
				print('You can now proceed to login')
				signIn()
def checkInArray():
	global mainArray
	global accountNumber
	global accountNotPresent
	if not any(val['accountNumber'] == accountNumber for val in mainArray):
		accountNotPresent = True
	else:
		accountNotPresent = False
def notANumber():
	print('Type in a number')
	numberAndPin()
def signIn():
	verifyContinue= ['continue with login', 'Register']
	for x in verifyContinue:
		print(str(verifyContinue.index(x) + 1) +  ' '+ x)
	loginChoose = selectOne()
	print(loginChoose)
	if loginChoose == '1':
		login()
	elif loginChoose== '2':
		registration()
	else:
		print('Invalid entry')
		signIn()
def login():
	global accountNumber, pin, loggedInUser, userId, mainArray
	userNumber = input('input your account number')
	userPin = input('input your pin')
	for i, val in enumerate(mainArray):
		if str(val['accountNumber']) == userNumber and str(val['pin']) == userPin:
			loggedInUser = val
			userId = i
			print('Logged in')
			mainMenu()
			return
	print('incorrect login details')
	signIn()
def mainMenu():
	homeSelect = ['withdrawal', 'transfer', 'enquiries']
	for x in homeSelect:
		print(str(homeSelect.index(x) + 1) +  ' '+ x)
	menuSelect = selectOne()
	if menuSelect == '1':
		withdrawFunc()
	elif menuSelect == '2':
		transferfunc()
	elif menuSelect == '3':
		enquiriesFunc()
	else:
		returnToHome()	
def returnToHome():
	print('invalid entry')
	returnHome = ['Main Menu', 'logout']
	print(str(returnHome.index(x) + 1) +  ' '+ x)
	chooseReturnHome = selectOne()
	if chooseReturnHome == '1':
		mainMenu()
	elif chooseReturnHome == '2':
		print('You have successfully logged out')
		signIn()
	else:
		returnToHome()
def selectOne():
	return input('select one')
def withdrawFunc():
	amountToWithdraw = [1000, 5000, 10000, 'other Amount']
	for x in amountToWithdraw:
		print(str(amountToWithdraw.index(x) + 1) +  ' '+ str(x))
	withdrawAmount = selectOne()
	if withdrawAmount == '1' or withdrawAmount == '2' or withdrawAmount == '3':
		checkWithdrawAmount(amountToWithdraw[convertIntToString(withdrawAmount)-1])

	elif withdrawAmount == '4':
		try:
			amountTyped = int(input('input the amount you want to withdraw'))
		except:
			print('Only Numbers are accepted')
			withdrawFunc()
		else:
			checkWithdrawAmount(amountTyped)
		
		
	else:
		returnToHome()
def convertIntToString(param):
	params = int(param)
	return params
def anotherTransaction():
	global loggedInUser
	print('Do you want to perform another transaction')
	newTransaction = ['yes', 'no']
	for x in newTransaction:
		print(str(newTransaction.index(x) + 1) +  ' '+ str(x))
	verifyTransaction = selectOne()
	if verifyTransaction == '1':
		mainMenu()
	elif verifyTransaction == '2':
		print('Thank you for banking with us {}'.format(loggedInUser['name']))
		signIn()
	else:
		returnToHome()
def checkWithdrawAmount(amount):
	global amountAtHand
	if amount <= loggedInUser['amountAtHand']:
		loggedInUser['amountAtHand'] -= amount
		mainArray[userId] = loggedInUser
		val = '''You have successfully withdrawn {} from your account, 
			your current balance is {}'''
		print(val.format(amount, loggedInUser['amountAtHand']))
		anotherTransaction()
	else:
		insufficient('withdraw')
def insufficient(transactType):
	print('insufficient funds')
	myStr = transactType + " lesser amount"
	myArr = [myStr, 'Go back to the main menu']
	for x in myArr:
		print(str(myArr.index(x) + 1) +  ' '+ x)
	menuOrAmount = selectOne()
	if menuOrAmount == '2':
		mainMenu()
	elif menuOrAmount == '1' and transactType=='withdraw':
		withdrawFunc()
	elif menuOrAmount == '1' and transactType=='transfer':
		transferfunc()
	else:
		returnToHome()
def enquiriesFunc():
	global loggedInUser
	accountType = ['savings', 'current']
	for x in accountType:
		print(str(accountType.index(x) + 1) +  ' '+ x)
	selectedAccountType = selectOne()
	if selectedAccountType == '1' or selectedAccountType == '2':
		print('Your account balance is #{}'.format(loggedInUser['amountAtHand']))
		anotherTransaction()
	else:
		returnToHome()
def transferfunc():
	global loggedInUser
	global mainArray
	transferAccount =  int(input('Input receiver\'s account number'))
	amountToTransfer = int(input('Input the amount you want to transfer'))
	if loggedInUser['amountAtHand'] >= amountToTransfer:
		if not any(l['accountNumber'] == transferAccount for l in mainArray):
			print('This account does not exist')
			transferfunc()
			return
		else:
			for i, val in enumerate(mainArray):
				if transferAccount == val['accountNumber']:
					val['amountAtHand'] += amountToTransfer
					mainArray[i] = val
					print('Your transfer of #{} to {} was successful'.format(amountToTransfer, val['name']))
					loggedInUser['amountAtHand'] -= amountToTransfer
					mainArray[userId] = loggedInUser
					anotherTransaction()
	else:
		insufficient('transfer')
registration()