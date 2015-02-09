import requests
import sys
from BeautifulSoup import BeautifulSoup

config = open('config.txt', 'r')

try:
	line = config.readline()
except:
	print "No config.txt credentials file found. Please read exampleconfig.txt"

line = line.split(':')
username = line[0]
password = line[1].strip('\n')

payload = {
	'username': username,
	'password': password
}

with requests.Session() as c:
	print "[*] Logging in to okcupid with username: " + username
	r = c.post('https://m.okcupid.com/login', data=payload)
	r = c.get('https://m.okcupid.com/home')
	
	if "Sorry, your info was incorrect." in r.content:
		print "[-] Login failed, bad credentials."
	else:
		print "[+] Successful Login"
	#soup = BeautifulSoup(r.content)
	#print soup.prettify()
