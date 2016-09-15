import psycopg2
import sys

def createDBConnection():
	con = None
	try:
		#con = psycopg2.connect(database='magswitchDB', user='andrewgentry')  # For use on localhost
		con = psycopg2.connect(database='AppDB', user='admin-gentry')   # For deployed use only
		print "Connected to the DB successfully"

	except psycopg2.OperationalError as e:
		print('Unable to connect!\n{0}').format(e)
		sys.exit(1)

	finally:
		return con

def addUserToDB(firstName,lastName,email,distributor,salesperson,admin,interest,psswrd):
	con = createDBConnection()
	print("#####Adding interest:  %s   to database"%interest)

	try:
		cur = con.cursor()
		cur.execute("SELECT userID FROM users ORDER BY userID DESC LIMIT 1")
		lastUserID = cur.fetchone()
		nextUserID = lastUserID[0] + 1
		cur.execute("INSERT INTO users VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (firstName, lastName, email, distributor, salesperson, admin, psswrd, nextUserID, '{}', 1, interest))
		con.commit()
		print ("Added " + firstName + " to the database.")

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