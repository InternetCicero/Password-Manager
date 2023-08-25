# ---- Password Manager with Python and SQL -----

# ---> Imported Libaries <---
from cryptography.fernet import Fernet #--> libary for en/decryption
import mysql.connector #--> libary for database storage
import string #--> Libary for list of character for suggestions
import random #--> Libary for random number to genrate suggestions randomly



#Main menu actions --> 1

def Choose_Action():
	Action = input("Choose: Add/Select/Delete? ")

	if Action == "Add":

		need_sug = True

		while need_sug == True:
			sug = input("Do you want a suggestion (Y/N):  ")

			if sug == "Y" or sug == "y":
				get_Suggestion()
				need_sug = False

			elif sug == "N" or sug == "n":
				need_sug = False
			else: print("That is not an valid input? ^^ ")

		add_to_db(encrypt_Password(add_Password()), connectDb())

	elif Action == "Select":
		needed = input("Get password for which website or account: ")
		decrypt_Password(connectDb(), needed)

	elif Action == "Delete":

		needed = input("Which Account to you want to delete? ")
		delete_of_db(connectDb(), needed)


#Password Suggestions --> 7

def get_Suggestion():
	#Create possible characters
	possibleCharactersDict = {
		'capChar': list(string.ascii_uppercase), 
		'lowChar': list(string.ascii_lowercase),
		'num': list(str(range(0, 10))),
		'otherSymbols': list("!@&%/?#.,")
	}

	passwordLength = 8#int(input("Password Length: "))


	#Make list of all characters possible
	allCharacters = []

	for key, value in possibleCharactersDict.items():
		allCharacters.extend(value)

	#Suggest random password
	suggestedPassword = ''.join(random.choices(allCharacters, k=passwordLength))
	print(f"Suggested password: {suggestedPassword} \nFeel free to copy :)")
	return suggestedPassword




#Password Input --> 2

def add_Password(): #---> get input for a new password <---
	CheckForInput = False

	AccUse = input("What is the account used for? ")

	#Ask for username and password until they meet requirements
	while CheckForInput == False:
		print("Username should have 3-15 characters, spaces are not alowed!\nPassword needs 6-20 characters, spaces are not alowed!")

		newUsername = input("Type Username: ")
		newPassword = input("Type Password: ")

		# --> Check if password and username meet requirements
		if (len(newUsername) <  3) or (len(newUsername) > 15) or (" " in newUsername):
			print("Invalid Username!")
		if (len(newPassword) <  6) or (len(newUsername) > 20) or (" " in newPassword):
			print("Invalid Password!")
		else:
			CheckForInput = True

	return newUsername, newPassword, AccUse


#Password Encryption --> 3

def encrypt_Password(newData): # ---> Encrypt the password and username + store keys for decryption <---
	username, password, AccUse = newData

	# --> Generate key for password
	keyForPassword = Fernet.generate_key()
	fernetPassword = Fernet(keyForPassword)
	encryptedPassword = fernetPassword.encrypt(password.encode())

	#Generate key for username
	keyForUsername = Fernet.generate_key()
	fernetUsername = Fernet(keyForUsername)
	encryptedUsername = fernetUsername.encrypt(username.encode())

	return encryptedUsername, keyForUsername, encryptedPassword, keyForPassword, AccUse



#Connect to Db --> 4

def connectDb(): #---> Connect to the database <---
	PasswordRequired = True

	print("Connecting...")

	#Ask for password until given
	while PasswordRequired == True:
		PwForDb = input("Required password for database access! -> ")

		try:
			PwmDb = mysql.connector.connect(
				host = "localhost", #host
				password = PwForDb, #your password for the database
				database = "PasswordManager" #name of the database
				)

			PasswordRequired = False
		except:
			print("Wrong password! Please try again.")

	print(f"Connected to database!")

	return PwmDb

#Password Storage --> Database actions --> 5

def create_table(PwmDb): #---> Error handling to check if table exsists <---
	cursor = PwmDb.cursor()

	try:
		cursor.execute("CREATE TABLE Passwords (id INT AUTO_INCREMENT PRIMARY KEY, EncryptedUsername VARCHAR(255), EncryptedPassword VARCHAR(255), KeyForUsername VARCHAR(255), KeyForPassword VARCHAR(255), AccountFor VARCHAR(255))")
	except mysql.connector.Error as err:
		pass


def add_to_db(encryptedData, PwmDb): #---> Make an entry to the database <---
	username, keyUsername, password, keyPassword, AccUse = encryptedData
	cursor = PwmDb.cursor()

	create_table(PwmDb)

	command = "INSERT INTO Passwords (EncryptedUsername, EncryptedPassword, KeyForUsername, KeyForPassword, AccountFor) VALUES (%s, %s, %s, %s, %s)"
	cursor.execute(command, (username, password, keyUsername, keyPassword, AccUse))

	PwmDb.commit()


def delete_of_db(PwmDb, needed): #---> Delete an entry of database <---
	cursor = PwmDb.cursor()

	testCommand = "SELECT * FROM Passwords WHERE AccountFor = %s"
	cursor.execute(testCommand, (needed,))

	row = cursor.fetchone()

	if row:
		command = "DELETE FROM Passwords WHERE AccountFor = %s"
		cursor.execute(command, (needed,))

		PwmDb.commit()

	else:
		print("No entry found for the specified account.")



#Password Decryption and selecting the account info --> 6

def decrypt_Password(PwmDb, needed):
	cursor = PwmDb.cursor()

	command = "SELECT * FROM Passwords WHERE AccountFor = %s"
	cursor.execute(command, (needed,))
	
	row = cursor.fetchone()

	if row:
		print("Username and password is beeing decrypted...")
		rowId, EncryptedUsername, EncryptedPassword, KeyForUsername, KeyForPassword, AccountFor = row

		fernet_username = Fernet(KeyForUsername)
		decryptedUsername = fernet_username.decrypt(EncryptedUsername).decode()

		fernet_password = Fernet(KeyForPassword)
		decryptedPassword = fernet_password.decrypt(EncryptedPassword).decode()

		print("Decrypted Username:", decryptedUsername)
		print("Decrypted Password:", decryptedPassword)

		return decryptedUsername, decryptedPassword
	else:
		return("No entry found for the specified account.")

	cursor.close()


#GUI --> 8

def main(): #---> Main function <---
	#add_to_db(encrypt_Password(add_Password()), connectDb())
	Choose_Action()
	
	
if __name__ == "__main__":
	main()
