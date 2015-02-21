from okdigger import OKDigger
import logging
import sys
from db import okdatabase
import time

print """
#######################################
#        Freelance Sociology          #
#######################################
"""

totalUsers = 10000
dugUsers = 0

runningAverage = [] # running average of how long it takes per user

# Set logging level. Options: INFO, DEBUG, WARNING, ERROR
logging.basicConfig(stream=sys.stderr, filename='.okdigger.log', level=logging.DEBUG)

print "[*] Initializing database"
db = okdatabase.OKDatabase('everyone.db') # create and name database object
#db.destroyDatabase() # destroy old tables, comment out if running multiple times on same database
db.initDatabase() # create empty database
print "[+] Database initialized"

output = True # show output from searches

startTime = time.time()


print "[*] Logging in"
r = OKDigger()
if r.login(): #login, yo
	print "[+] Login successful"
	r.setSearchParams('everyone') # set search parameters from searches.py
	
	while dugUsers < totalUsers:

		print "[*] Digging usernames"
		users = r.getUsernames(50, output)  # get usernames using search parameters
	
		for user in users:
			userStart = time.time()
		
			if not db.checkUserExists(user, output): # make sure we haven't already scraped user

				details = r.getUserDetails(user, output) # scrape user details
				answers = r.getUserAnswers(user, output) # scrape user answers
				db.addUserDetails(user, details, output) # add details to db
				db.addUserAnswers(user, answers, output) # ad answers to db

				dugUsers += 1

				# update time variables
				userTime = time.time() - userStart
				runningAverage.append(int(userTime))
				average = reduce(lambda x, y: x+y, runningAverage)/len(runningAverage)
				left = len(users) - users.index(user)
				remaining = average * left
				minutes = remaining = remaining/60
				remainder = minutes % 60
				hours = int(minutes/60)
				print " [t] " + str(hours) + " hours and " + str(remainder) + " minutes left, " + str(users.index(user)) + " of " + str(len(users)) + " users dug (" + str(average) + " seconds per user)"
				time.sleep(r.randomDelay())

else:
	print "[-] Error: couldn't log in, bad credentials or connection."

print '[+] Done. Completed in ' + str(int(time.time() - startTime)/60) + ' minutes.'
