"""
OKDigger.py

A Class with a set of tools to scrape OKCupid site data. 

"""

import requests
import sys
import time
from BeautifulSoup import BeautifulSoup
import searches
import logging

class OKDigger:

	def __init__(self):
		self.session = requests.Session()
		self.search_url = ""
	
	# Login function returns requests Session object to logged-in okcupid session. 
	# If login is not successful, returns 0.
	def login(self):
		config = open('config.txt', 'r')

		try:
			line = config.readline()
		except:
			logging.error("No config.txt credentials file found. Please read exampleconfig.txt")

		line = line.split(':')
		username = line[0]
		password = line[1].strip('\n')

		payload = {
			'username': username,
			'password': password
		}

		with requests.Session() as c:
			r = c.post('https://m.okcupid.com/login', data=payload)
			r = c.get('https://m.okcupid.com/home')
		
			if "Sorry, your info was incorrect." in r.content:
				logging.error("[-] Bad credentials or bad connection. Could not log in.")
				return 0
			else:
				self.session = c
				return c
	
	# Returns html of quickmatch link
	def quickmatch(self):
		c = self.session
		r = c.get('https://m.okcupid.com/quickmatch')
		return r.text
	
	# Finds user profile page for username 'user'
	# Returns page html
	# Returns 0 on failure
	def getProfile(self, user):
		c = self.session
		url = 'http://m.okcupid.com/profile/' + user + '?cf=regular'
		r = c.get(url)
		if "Account Not Found" in r.text:
			logging.error("Could not find user " + user)
			return 0
		else:
			return r.text
	
	# Returns a list of num_usernames usernames
	def getUsernames(self, num_usernames, output = False):
		
		c = self.session
		usernames = []
		total = 0
		index = 1
		
		while total < num_usernames:
			url = 'http://m.okcupid.com/match?low=' + str(index) + '&timekey=10&template_style='
			time.sleep(1) # Delay so we don't trigger policebots
			r = c.get(url)
			soup = BeautifulSoup(r.text)
		
			# Grab the usernames
			searched = soup.findAll('a', 'username')
			if searched == []:
				return usernames
			for item in searched:
				unicodename = item.contents
				name = str(unicodename)[3:-2]
				usernames.append(name)
				total += 1
			index = index + 9
			if output:
				print '[*] Dug ' + str(len(usernames)) + ' of ' + str(num_usernames) + ' users' 
		return usernames[:num_usernames]

	# Returns dictionary of details for user in form attribute:answer
	# Returns 0 on failure to find user
	def getUserDetails(self, user):
		i = 0
		results = {}
		attributes = []
		answers = []
		raw = self.getProfile(user)
		if raw == 0:
			logging.error("Could not get details for " + user)
			return 0
		soup = BeautifulSoup(raw)
		
		# Dig out attribute list
		searched_attributes = soup.findAll('span', 'label')
		for line in searched_attributes:
			attributes.append(str(line.contents)[3:-2])

		# Dig out answers list
		searched_answers = soup.findAll('span')
		for line in searched_answers:
			if (i % 2) == 1 and i < 36:
				answers.append(str(line.contents)[3:-2])
			i += 1

		# Pack into dictionary
		for x in range(0,len(attributes)):
			results[attributes[x]] = answers[x]
		return results

	# Returns dictionary of questions and answers in form question: answer
	# Returns 0 on failure to find user
	def getUserAnswers(self, user, num_answers, output = False):
		c = self.session
		question_list = []
		answer_list = []
		results = {}
		index = 1
		repeat = 0
		old_list_len = 0
		threshold = 0
		
		if output:
			print '[*] Digging answers for user ' + user
		while index <= 1031 and threshold < 3:
			r = c.get('http://m.okcupid.com/profile/' + user +'/questions?low=' + str(index) + '&n=9')
			soup = BeautifulSoup(r.text)
			questions = soup.findAll('div', 'question public clearfix')
			for question in questions:
				question_list.append(str(question.h3.contents)[3:-2])
				answer_list.append(str(question.p.span.contents)[5:-4])
			questions = soup.findAll('div', 'question public talk clearfix')
			for question in questions:
				question_list.append(str(question.h3.contents)[3:-2])
				answer_list.append(str(question.p.span.contents)[5:-4])
			index += 10
			if len(answer_list) == old_list_len:
				threshold += 1
			else:
				old_list_len = len(answer_list)
			time.sleep(1)
			if len(answer_list) >= num_answers:
				break
			if output:
				print '[*] Dug ' + str(len(answer_list)) + ' of ' + str(num_answers) + ' answers'
		
		for x in range(0, len(answer_list)):
			results[question_list[x]] = answer_list[x]
		return results

	def setSearchParams(self, search_type):
		self.search_url = searches.searches[search_type]
		c= self.session
		c.get(self.search_url)



	
