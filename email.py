import os
import db
import time

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
cur.execute("SELECT newusers FROM stats")
oldHigh = cur.fetchall()
newusers = thisHigh[0] - sum(oldHigh[0])
print(newusers)

cur.execute("SELECT logincount FROM users")
logins = cur.fetchall()

someList = [] 
for i in logins:
	someList.append(i[0])

newCount = sum(someList)

cur.execute("SELECT logins, entry FROM stats ORDER BY entry DESC LIMIT 1")  #while we're in the stats table might as well grab the last entry too
lastCount = cur.fetchone()
lastEntry = lastCount[1]
weeklyLogins = newCount - lastCount[0]
print(weeklyLogins)

#each time we run this script we want to post it's results in the stats table and stamp the date on it
date = time.strftime("%c")
cur.execute("INSERT INTO stats VALUES(%s, %s, %s, %s, %s)" ,(lastEntry+1, date, newusers, weeklyLogins, weeklyproduct))
con.commit()

os.system("echo \"Hey everybody! Here are the statistics for the Mobile App over the past week.\n\nMost Viewed Product: %s \n\nNumber of new users: %s \n\nNumber of logins: %s\" | mail -s \"Weekly Stat Update\" agentry@magswitch.com.au"%(weeklyproduct[0], newusers, weeklyLogins))
