from okdigger import OKDigger
import logging
import sys
from db import okdatabase

# Set logging level. Options: INFO, DEBUG, WARNING, ERROR
logging.basicConfig(stream=sys.stderr, filename='.okdigger.log', level=logging.DEBUG)
"""
db = okdatabase.OKDatabase('details.db')
db.dropTable('Details')
db.initDatabase()

output = True

r = OKDigger()
if r.login():
	r.setSearchParams('everyone')
	users = r.getUsernames(10, output)
	for user in users:
		answers = r.getUserDetails(user, output)
		db.addUserDetails(user, answers)
"""
r = OKDigger()
if r.login():
	print r.getUserAnswers('va2co', True)

