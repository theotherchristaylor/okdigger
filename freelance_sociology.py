"""
freelance_sociology.py

A utility to run the OKDigger tools

Written by Chris Taylor, 3/5/15
"""

import sys
import searches
import build_database

def getChoice():
	sys.stdout.write("Choice: ")
	choice = raw_input()
	return choice

def printMenu():
	print """################################################################
Freelance Sociology

(1) Build database
(2) Run overall report (The Crunch)
(3) Get ages data
(4) Get deviations report
"""
	choice = getChoice()

	if choice == '1':
		buildDatabase()

def buildDatabase():
	print ""
	print "Select search parameters to use:"
	index = 1
	searchesList = searches.searches.keys()
	for search in searchesList:
		print '(' + str(index) + ')' + search
		index += 1
	print ""
	choice = int(getChoice()) - 1
	print "Building database with search " + searchesList[choice]
	search = searchesList[choice]
	sys.stdout.write("Enter name of new or existing database: ")
	databaseName = raw_input()
	print "Using database " + databaseName
	build_database.buildDatabase(search, databaseName)
printMenu()
