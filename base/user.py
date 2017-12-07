import db
import sys
import time

class User:

	def __init__(self, userid):
		try:
			con = db.createDBConnection()
			cur = con.cursor()
			cur.execute("SELECT firstname, lastname, email, distributor, salesperson, admin, logincount, interest FROM users WHERE userid = %s", (userid,))
			results = cur.fetchone()

			self.firstName = results[0]
			self.lastName = results[1]
			self.email = results[2]
			self.distributor = results[3]
			self.salesperson = results[4]
			self.admin = results[5]
			self.logincount = results[6]
			self.userid = userid
			self.interest = results[7]
			self.lastLogin = "7-20-2016"

			print("New user created: " + self.firstName + " " + self.lastName)

		except:
			print("Unexpected error:", sys.exc_info()[0])
			raise

	def incrementLoginCount(self):
		try:
			con = db.createDBConnection()
			cur = con.cursor()
			cur.execute("SELECT logincount FROM users WHERE userid = %s", (self.userid,))
			oldcount = cur.fetchone()
			newcount = oldcount[0] + 1
			print("New count is: %s", (newcount))
			cur.execute("UPDATE users SET logincount = %s WHERE userid = %s", (newcount, self.userid))
			con.commit()
			print("incremented fine")

		except Exception as err:
			print(err)

	def updateHistory(self):
		try:
			con = db.createDBConnection()
			cur = con.cursor()
			date = time.strftime("%c")
			cur.execute("UPDATE users SET lastlogin = %s WHERE userid = %s", (date, self.userid))
			con.commit()
			print("Updated User Login Date")

		except Exception as err:
			print(err)

