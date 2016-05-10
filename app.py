from flask import Flask, jsonify, session, request, redirect
import psycopg2
from prettytable import PrettyTable
import bcrypt
from bcrypt import hashpw, gensalt

app = Flask(__name__)

class User:

	def __init__(self, firstName, lastName, email, distributor, salesperson, admin, psswrd):
		try:
			self.firstName = firstName
			self.lastName = lastName
			self.email = email
			self.distributor = distributor
			self.salesperson = salesperson
			self.admin = admin
			self.psswrd = psswrd
			print("New user created: " + self.firstName + " " + self.lastName)

		except:
			print("Unexpected error:", sys.exc_info()[0])
			raise

class Bug:

	def __init__(self, description, date, device):
		self.description = description
		self.date = date
		self.device = device	
		print("new bug found")

def isLoggedin():
	try:
		if session["loggedin"] == True:
			return True
		else:
			return False

	except:
		return False

# create the vars that we use for the sessions
def createSession(userID):
	session["loggedin"] = True
	session["userID"] = userID

def hashPassword(psswrd):
	return bcrypt.hashpw(psswrd.encode(), bcrypt.gensalt().encode())

def checkPassword(passwrd, hashedPass):
	return hashedPass.encode() == bcrypt.hashpw(passwrd.encode(), hashedPass.encode())

def createDBConnection():
	con = None
	try:
		con = psycopg2.connect(database='AppDB', user='admin-gentry')
		print "connected to the DB successfully"
	except psycopg2.DatabaseError as e:
		print "Connection Error." + e
		sys.exit(1)

	finally:
		return con

def addUserToDB(newUser):
	con = createDBConnection()

	try:
		cur = con.cursor()
		cur.execute("SELECT userID FROM users ORDER BY userID DESC LIMIT 1")
		print("Selct Executed")
		lastUserID = cur.fetchone()
		print(lastUserID[0])
		nextUserID = lastUserID[0] + 1
		cur.execute("INSERT INTO users VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (newUser.firstName, newUser.lastName, newUser.email, newUser.distributor, newUser.salesperson, newUser.admin, newUser.psswrd, nextUserID))
		con.commit()
		print ("Added '" + newUser.firstName + " to the database.")

	except psycopg2.DatabaseError as e:

		print "Error adding a user." + e

		if con:
			con.rollback
		sys.exit(1)

	finally:
		if con:
			con.close

		return

def addBugToDB(newBug):
	con = createDBConnection()

	try:
		cur = con.cursor()
		cur.execute("INSERT INTO bugs VALUES(%s,%s,%s)", (newBug.description, newBug.date, newBug.device))
		con.commit()
		print("Added a Bug to the DataBase")

	except psycopg2.DatabaseError as e:
		print "Error adding a bug." + e

	finally:
		if con:
			con.close

		return


@app.route('/create/', methods=['POST'])
def createUser():
	if request.method == 'POST':

		print("Recived a POST request")
		firstName = request.form['firstName']
		lastName = request.form['lastName']
		email = request.form['email']
		distributor = request.form['distributor']
		salesperson = request.form['salesperson']
		admin = request.form['admin']

		psswrd = request.form['psswrd']
		hashed = hashPassword(psswrd)

		newUser = User(firstName,lastName,email,distributor,salesperson,admin,hashed)
		addUserToDB(newUser)

		return 'Created A User'

	else:
		return status.HTTP_405_METHOD_NOT_ALLOWED

@app.route('/bug/', methods=['POST'])
def bugReport():
	if request.method == 'POST':
		description = request.form['description']
		date = request.form['date']
		device = request.form['device']
		newBug = Bug(description, date, device)
		addBugToDB(newBug)
	
		print "Added a Bug"
		return "Added bug"

	else:
		return status.HTTP_405_METHOD_NOT_ALLOWED

@app.route('/')
def index():
	print "Accessed the server"
	return redirect('http://www.magswitch.com.au')

app.secret_key = '087c38712m]43jvdsp[ew'
@app.route('/login/', methods=['GET','POST'])
def checkLogin():
	if request.method == 'GET':
		
		if isLoggedin():
			return "True"
		else:
			return '''
	
					<form action = "" method = "post">
						<p>Email: <input type ="text" name ="email" /></p>
						<p>Password: <input type ="text" name ="psswrd_attempt" /></p>
						<p><input type ="submit" value = "Login" /></p>
					</form>
	
					'''


	if request.method == 'POST':
		email = request.form['email']
		psswrd_attempt = request.form['psswrd_attempt']

		con = createDBConnection()
		cur = con.cursor()
		print("created cursor")
		print(email)

		cur.execute("SELECT psswrd, userid FROM users WHERE \"email\" = %s", (email,))
		
		results = cur.fetchone()
		validCredentials = False

		print(results[0])
		print(results[1])

		try:
			if checkPassword(psswrd_attempt, results[0]):
				validCredentials = True
				createSession(results[1])
				print("created session")
			else:
				print("checkPassword didn't return true")

		except:
			pass

		if validCredentials:
			print("Logged in fine")
			return "Welcome!"
		else:
			print("bad password")
			return "Unauthorized"

	else :
		return "Invalid Request Type"

@app.route("/logout/", methods=["GET"])
def removeSession():
	session["loggedin"] = False
	session.clear()
	return "Logged Out"

@app.route("/favorite/", methods=["GET", "POST"])
def favorite():

	if isLoggedin():
		return session["userID"]
	else:
		redirect('/login/')


if __name__ == '__main__':
	app.run(DEBUG=True)

