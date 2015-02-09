import requests
import sys
from BeautifulSoup import BeautifulSoup


payload = {
	'username': 'fakeusername',
	'password': 'fakepassword'
}

with requests.Session() as c:
	r = c.post('https://m.okcupid.com/login', data=payload)
	print r.status_code
	r = c.get('https://m.okcupid.com/home')
	
	if "Sorry, your info was incorrect." in r.content:
		print "Login failed"
	else:
		print "Potential success."
	soup = BeautifulSoup(r.content)
	print soup.prettify()
