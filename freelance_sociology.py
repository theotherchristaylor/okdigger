from okdigger import OKDigger
import logging
import sys

# Set logging level. Options: INFO, DEBUG, WARNING, ERROR
logging.basicConfig(stream=sys.stderr, filename='.okdigger.log', level=logging.DEBUG)


output = False

r = OKDigger()
if r.login():
	r.setSearchParams('everyone')
	print '[*] Digging 50 usernames'
	users = r.getUsernames(50, output)
	for user in users:
		f = open('./users/' + user + '.okc', 'w')
		print '[*] Digging answers for user ' + user
		answers = r.getUserAnswers(user, 100, output)
		f.write(str(answers))
		f.close()

