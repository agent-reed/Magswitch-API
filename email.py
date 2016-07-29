import os
import db

con = db.createDBConnection()
cur = con.cursor()
#reset the weekly views of the products after grabbing the highest. This script runs once a week.
cur.execute("SELECT name FROM products ORDER BY weeklyviews DESC LIMIT 1")
weeklyproduct = cur.fethone()


os.system("echo \"This is a test email from the app server\" | mail -s \"%s\" agentry@magswitch.com.au", (weeklyproduct,))


