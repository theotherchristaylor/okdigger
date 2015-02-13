from okdigger import OKDigger

r = OKDigger()
if r.login():
	r.setSearchParams('everyone')
	users = r.getUsernames(50, True)
	for user in users:
		f = open('./users/' + user + '.okc', 'w')
		print '[*] Digging answers for user ' + user
		answers = r.getUserAnswers(user, 100, True)
		f.write(str(answers))
		f.close()

