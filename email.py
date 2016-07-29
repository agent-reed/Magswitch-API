import os
import db

con = db.createDBConnection()
cur = con.cursor()

#grab the product name with the highest weekly views
cur.execute("SELECT name FROM products ORDER BY weeklyviews DESC LIMIT 1")
weeklyproduct = cur.fetchone()

#reset the weekly views of the products after grabbing the highest. This script runs once a week.
cur.execute("UPDATE products SET weeklyviews = 0")
con.commit()


cur.execute("SELECT userid FROM users ORDER BY userid DESC LIMIT 1")
thisHigh = cur.fetchone()

cur.execute("SELECT newusers FROM stats ORDER BY newusers DESC LIMIT 1")
oldHigh = cur.fetchone()

newusers = thisHigh - oldHigh


os.system("echo \"This week, the most popular product was: %s \n Number of new users : %s \" | mail -s \"Weekly Stat Update\" agentry@magswitch.com.au"%(weeklyproduct, newusers))



