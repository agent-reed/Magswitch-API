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

#grab the highest userid this week
cur.execute("SELECT userid FROM users ORDER BY userid DESC LIMIT 1")
thisHigh = cur.fetchone()

#grab the highest userid that has been stored in stats.  we know the difference between the two is the number of new users. 
cur.execute("SELECT newusers FROM stats ORDER BY entry DESC LIMIT 1")
oldHigh = cur.fetchone()
newusers = thisHigh[0] - oldHigh[0]

cur.execute("SELECT logincount FROM users")
logins = cur.fetchall()

someList = [] 
for i in logins:
	someList.append(i[0])

newCount = sum(someList)
print(newCount)

cur.execute("SELECT logins FROM stats ORDER BY entry DESC LIMIT 1")
lastCount = cur.fetchone()

weeklyLogins = newCount - lastCount[0]

os.system("echo \"This week, the most viewed product was: %s \n Number of new users : %s \n Number of Logins this week: %s\" | mail -s \"Weekly Stat Update\" agentry@magswitch.com.au"%(weeklyproduct[0], newusers, weeklyLogins))



