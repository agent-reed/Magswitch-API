from flask import Flask, jsonify, request, redirect
import psycopg2
from prettytable import PrettyTable

app = Flask(__name__)

class User:

    def __init__(self, name, psswrd, email, distributor, salesperson):
        self.name = name
        self.psswrd = psswrd
        self.email = email
        self.distributor = distributor
        self.salesperson = salesperson
        self.favorites = [] 

        print ("new user created: " + self.name)

    def add_favorite(self, trick):
        self.favorites.append(favorite)

class Bug:

    def __init__(self, description, date, device):
        self.description = description
        self.date = date
        self.device = device

        print("new bug found")


con = None
def createDBConnection():

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
		cur.execute("INSERT INTO users VALUES(%s,%s,%s,%s,%s)", (newUser.name, newUser.psswrd, newUser.email, newUser.distributor, newUser.salesperson))
		con.commit()
		print ("Added '" + name + " to the database.")

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

		name = request.form['username']
		psswrd = request.form['psswrd']
		email = request.form['email']
		distributor = request.form['distributor']
		salesperson = request.form['salesperson']
		print "processed form"

		newUser = User(name,psswrd,email,distributor,salesperson)
		addUserToDB(newUser)

		return 'Created A User'

	else:
		return status.HTTP_405_METHOD_NOT_ALLOWED

@app.route('/bug/', methods=['POST'])
def bugReport():
	if request.method == 'POST':
		print "Recieved Request"
	
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


@app.route('/test')
def testConnect():
		
	try:
		con = createDBConnection()
		cur = con.cursor()
		cur.execute('SELECT version()')          
		ver = cur.fetchone()
		print ver    

	except psycopg2.DatabaseError, e:
		print 'Error %s' % e    
		sys.exit(1)

	finally:

		if con:
			con.close()	
    
    

@app.route('/data/')
def names():
	
	con = createDBConnection()

	try:
		cur = con.cursor()
		cur.execute("SELECT * FROM users")
		t = PrettyTable(['|______First Name______|', '|______Last Name______|', '|________.Email._________|', '|___.Distributor.___|', '|___.Salesperson.__|'])
		for record in cur:
			t.add_row([record[0],record[1],record[2],record[3],record[4]])
		return t.get_html_string()
		 

	except psycopg2.DatabaseError as e:

		if con:
			con.rollback

		print "Error displaying the users." + e
		sys.exit(1)



if __name__ == '__main__':
	app.debug = True
	app.run()

