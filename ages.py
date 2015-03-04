"""
ages.py

Output age distribution of users

Written by Chris Taylor, 3/3/14

"""

from db.okdatabase import OKDatabase

databaseName = "everyone_local.db"

db = OKDatabase(databaseName)

maleSampleSize = db.executeQuery('select count("Gender") from Details where "Gender"="Man"', 'fetchone')
femaleSampleSize = db.executeQuery('select count("Gender") from Details where "Gender"="Woman"', 'fetchone')

print "Age Men Women" 
for index in range(18,99):
	query = 'select count("Age") from Details where "Age"="' + str(index) + '" and "Gender"="Man" and "Location"="Boulder, Colorado"'
	maleAmount = db.executeQuery(query, 'fetchone')
	query = 'select count("Age") from Details where "Age"="' + str(index) + '" and "Gender"="Woman" and "Location"="Boulder, Colorado"'
	femaleAmount = db.executeQuery(query, 'fetchone')
	
	maleAmount = maleAmount[0]
	femaleAmount = femaleAmount[0]

	if maleAmount != 0 or femaleAmount != 0:
		print  str(index) + " " + str(maleAmount) + " " + str(femaleAmount)
