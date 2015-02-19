from okdigger import OKDigger
import logging
import sys
from db import okdatabase
import time

runningAverage = []


# Set logging level. Options: INFO, DEBUG, WARNING, ERROR
logging.basicConfig(stream=sys.stderr, filename='.okdigger.log', level=logging.DEBUG)

db = okdatabase.OKDatabase('everyone.db')
db.destroyDatabase()
db.initDatabase()

output = True

startTime = time.time()

r = OKDigger()
if r.login():
	r.setSearchParams('everyone')
	users = r.getUsernames(5, output)
	

	for user in users:
		userStart = time.time()
		
		if not db.checkUserExists(user):

			details = r.getUserDetails(user, output)
			answers = r.getUserAnswers(user, output)
			db.addUserDetails(user, details, output)
			db.addUserAnswers(user, answers, output)

			userTime = time.time() - userStart

			runningAverage.append(int(userTime))
			average = reduce(lambda x, y: x+y, runningAverage)/len(runningAverage)
			left = len(users) - users.index(user)
			remaining = average * left

			print ' [*] ' + str(int(remaining/60)) + ' minutes remaining.'

print '[+] Done. Completed in ' + str(int(time.time() - startTime)/60) + ' minutes.'
