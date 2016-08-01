from flask import Flask, jsonify, session, request, redirect

from user import User

import bcrypt
import db
import calcs

app = Flask(__name__)
app.debug = True

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
	print("Checking Password...")
	return hashedPass.encode() == bcrypt.hashpw(passwrd.encode(), hashedPass.encode())

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
			interest = request.form['interest']

			psswrd = request.form['psswrd']
			hashed = hashPassword(psswrd)

			db.addUserToDB(firstName,lastName,email,distributor,salesperson,admin,interest,hashed)

			return 'Created a User'

		except Exception as err:
			print(err)

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
		db.addBugToDB(newBug)
	
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
			userID = str(session["userID"])
			newUser = User(userID)
			newUser.incrementLoginCount()
			newUser.updateHistory()
			# return "Welcome!"
			return jsonify(firstname=newUser.firstName,lastname=newUser.lastName,email=newUser.email,distributor=newUser.distributor, salesperson=newUser.salesperson, admin=newUser.admin, userid=newUser.userid, logincount=newUser.logincount, interest=newUser.interest), 201

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

			con = db.createDBConnection()
			cur = con.cursor()
			cur.execute("SELECT psswrd, userid FROM users WHERE \"email\" = %s", (email,))
			print("Post Executed")
			results = cur.fetchone()
			print("Results Fetched: %s" %results[0])

			if results[0] and results [1] == None:
				return "No username in DB", 404

			if checkPassword(psswrd_attempt, results[0]):
				print("Password Checks Out")
				userID = results[1]
				createSession(userID)
				newUser = User(userID)
				newUser.incrementLoginCount()
				newUser.updateHistory()
				# return "Welcome!"
				return jsonify(firstname=newUser.firstName,lastname=newUser.lastName,email=newUser.email,distributor=newUser.distributor, salesperson=newUser.salesperson, admin=newUser.admin, userid=newUser.userid, logincount=newUser.logincount, interest=newUser.interest), 201
			else:
				print("Incorrect Combination")
				return "Unauthorized", 403

		except Exception as err:
			print(err)
			return "An error occured with logging in."


@app.route("/logout/", methods=['GET'])
def removeSession():
	session["loggedin"] = False
	session.clear()
	return "Logged Out"


@app.route("/product/", methods=['POST'])
def tagProduct():

	if request.method == 'POST':

		productid = request.form["productid"]
		name = request.form["name"]

		if isLoggedin():
			print("Somebody is logged in")
			userID = int(session["userID"])
			con = db.createDBConnection()
			cur = con.cursor()

			cur.execute("SELECT EXISTS(SELECT 1 FROM products WHERE productid=%s)", (productid,))
			result = cur.fetchone()
			if result[0] == False:
				cur.execute("INSERT INTO products VALUES(%s, %s, %s, %s, %s)", (productid, name, 1, 1, [userID,0]))
				con.commit()

			else:
				cur.execute("SELECT totalviews, users FROM products WHERE productid=%s", (productid,))
				result = cur.fetchone()
				total = result[0]
				users = result[1]
				print(users)
				print(userID)
				cur.execute("UPDATE products SET totalviews=%s WHERE productid=%s", (total+1, productid))

				if userID in users:
					print("User already in list")
				else:
					cur.execute("UPDATE products SET users = array_append(users,%s)", (userID,))

				con.commit()

			# cur.execute("UPDATE products SET totalviews=%s WHERE productid=%s", (23,productid))
			# cur.execute("INSERT INTO products (productid, name, totalviews) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM products WHERE productid=%s)", (productid, name, 24, productid))

			return "Okay"

		else:
			return "Not logged in"

@app.route("/favorite/", methods=['GET', 'POST'])
def favorite():

	if request.method == 'GET':
		if isLoggedin():
			print("Somebody is logged in")
			userID = str(session["userID"])
			con = db.createDBConnection()
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
			con = db.createDBConnection()
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
			con = db.createDBConnection()
			cur = con.cursor()
			print("About to execute")
			cur.execute("UPDATE users SET favorites = array_remove(favorites,%s) WHERE userid = %s", (productid,userID))
			con.commit()
			
			return "Removed from favorites"

		else:
			redirect('/login/')


@app.route("/calculate/", methods=['POST'])
def calculateHoldingForce():

	unit = request.form["unit"]
	material = request.form["material"]
	thickness = request.form["thickness"]

	if thickness < 0:
		print("Negative thickness given - Cannot Calculate")
		return "Invalid Input"

	holdingForce = calcs.holdingCalc(unit, material, thickness)

	print("Holding force is %s kg" % holdingForce)

	return holdingForce


if __name__ == '__main__':
	app.run()

