from flask import Flask, jsonify, session, request, redirect
import psycopg2
from prettytable import PrettyTable
import bcrypt
from bcrypt import hashpw, gensalt

app = Flask(__name__)
app.debug = True

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
		con = psycopg2.connect(host='localhost', database='magswitchDB', user='andrewgentry')
		print "Connected to the DB successfully"
		
	except psycopg2.OperationalError as e:
		print('Unable to connect!\n{0}').format(e)
		sys.exit(1)

	finally:
		return con

def addUserToDB(newUser):
	con = createDBConnection()

	try:
		cur = con.cursor()
		cur.execute("SELECT userID FROM users ORDER BY userID DESC LIMIT 1")
		lastUserID = cur.fetchone()
		nextUserID = lastUserID[0] + 1
		cur.execute("INSERT INTO users VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (newUser.firstName, newUser.lastName, newUser.email, newUser.distributor, newUser.salesperson, newUser.admin, newUser.psswrd, nextUserID))
		con.commit()
		print ("Added '" + newUser.firstName + " to the database.")

	except Exception as err:
		print(err)

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

	except psycopg2.OperationalError as e:
		print('Unable to connect!\n{0}').format(e)

	finally:
		if con:
			con.close

		return


@app.route('/create/', methods=['POST'])
def createUser():
	if request.method == 'POST':

		try:
			print("Recived a POST request under Create")
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

		except psycopg2.OperationalError as e:
			print('Unable to connect!\n{0}').format(e)

			return 'Unable to create a new user'

	else:
		return "Method Not Allowed"

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
		return "Method Not Allowed"

@app.route('/')
def index():
	return redirect('http://www.magswitch.com.au')

app.secret_key = '087c38712m]43jvdsp[ew'
@app.route('/login/', methods=['GET','POST'])
def checkLogin():
	if request.method == 'GET':
		
		if isLoggedin():
			return 'Welcome!'

		else:
			return '''
					<form action = "" method = "post">
						<p>Email: <input type ="text" name ="email" /></p>
						<p>Password: <input type ="text" name ="psswrd_attempt" /></p>
						<p><input type ="submit" value = "Login" /></p>
					</form>
	
					'''

	if request.method == 'POST':
		try:

			email = request.form['email']
			psswrd_attempt = request.form['psswrd_attempt']
			print("Email: " + email)

			con = createDBConnection()
			cur = con.cursor()
			cur.execute("SELECT psswrd, userid FROM users WHERE \"email\" = %s", (email,))
			results = cur.fetchone()
		
			if checkPassword(psswrd_attempt, results[0]):
				createSession(results[1])
				return "Welcome!", 201
			else:
				print("Incorrect Combination")
				return "Unauthorized", 401

		except Exception as err:
			print(err)
			return "An Error Occured"


@app.route("/logout/", methods=['GET'])
def removeSession():
	session["loggedin"] = False
	session.clear()
	return "Logged Out"

@app.route("/favorite/", methods=['GET', 'POST'])
def favorite():

	if request.method == 'GET':
		if isLoggedin():
			print("Somebody is logged in")
			userID = str(session["userID"])
			con = createDBConnection()
			cur = con.cursor()
			print("About to execute")
			cur.execute("SELECT favorites FROM users WHERE \"userid\" = %s", (userID,))
			print("executed")
			results = cur.fetchone()
			print("fetched")
			print(results[0])

			return str(results[0])
		else:
			return redirect('/login/')

	if request.method == 'POST':

		productid = request.form["productid"]

		if isLoggedin():
			userID = str(session["userID"])
			con = createDBConnection()
			cur = con.cursor()
			print("About to execute")
			cur.execute("UPDATE users SET favorites = array_append(favorites,%s) WHERE userid = %s", (productid,userID))
			con.commit()
			
			return "Added to favorites!"

		else:
			return redirect('/login/')

@app.route("/deleteFavorite/", methods=['POST'])
def deleteFavorite():

	if request.method == 'POST':

		productid = request.form["productid"]

		if isLoggedin():
			userID = str(session["userID"])
			con = createDBConnection()
			cur = con.cursor()
			print("About to execute")
			cur.execute("UPDATE users SET favorites = array_remove(favorites,%s) WHERE userid = %s", (productid,userID))
			con.commit()
			
			return "Removed from favorites"

		else:
			redirect('/login/')


if __name__ == '__main__':
	app.run()

