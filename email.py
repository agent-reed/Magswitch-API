import os
import db
import time

con = db.createDBConnection()
cur = con.cursor()

#grab the product name with the highest weekly views
cur.execute("SELECT name FROM products ORDER BY weeklyviews DESC")
weeklyproducts = cur.fetchmany(size=5)
print weeklyproducts
#reset the weekly views of the products after grabbing the highest. This script runs once a week.
cur.execute("UPDATE products SET weeklyviews = 0")
con.commit()

#grab the highest userid this week
cur.execute("SELECT userid FROM users ORDER BY userid DESC LIMIT 1")
thisHigh = cur.fetchone()

#grab the highest userid that has been stored in stats.  we know the difference between the two is the number of new users. 
cur.execute("SELECT newusers FROM stats")
oldHighList = cur.fetchall()

highList = []
for i in oldHighList:
	highList.append(i[0])
oldHigh = sum(highList)

newusers = thisHigh[0] - oldHigh

cur.execute("SELECT logincount FROM users")
logins = cur.fetchall()

someList = [] 
for i in logins:
	someList.append(i[0])
newCount = sum(someList)

cur.execute("SELECT logins, entry FROM stats ORDER BY entry DESC")  #while we're in the stats table might as well grab the last entry too
lastCountList = cur.fetchall()
lastEntry = lastCountList[0][1]

countList = []
for i in lastCountList:
	countList.append(i[0])
lastCount = sum(countList)

weeklyLogins = newCount - lastCount
print(weeklyLogins)

#each time we run this script we want to post it's results in the stats table and stamp the date on it
date = time.strftime("%c")
cur.execute("INSERT INTO stats VALUES(%s, %s, %s, %s, %s)" ,(lastEntry+1, date, newusers, weeklyLogins, weeklyproducts[0]))
con.commit()

os.system("echo \"Hey everybody! Here are the statistics for the Mobile App over the past week.\n\nMost Viewed Products: \n #1: %s \n #2: %s \n #3: %s \n #4: %s \n #5 %s \n\nNumber of new users: %s \n\nTotal Users Today: %s \n\nNumber of unique logins: %s\" | mail -s \"Weekly Stat Update\" -c andrew.gentry@colorado.edu agentry@magswitch.com.au"%(weeklyproducts[0][0], weeklyproducts[1][0], weeklyproducts[2][0], weeklyproducts[3][0], weeklyproducts[4][0], newusers, thisHigh[0][0], weeklyLogins))
