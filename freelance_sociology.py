"""
freelance_sociology.py

A utility to run the OKDigger tools

Written by Chris Taylor, 3/5/15
"""

import sys
import searches
import build_database
import thecrunch
import ages
import correlations

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
(5) Generate config.txt
"""
	choice = getChoice()

	if choice == '1':
		buildDatabase()
	elif choice == '2':
		runTheCrunch()
	elif choice == '3':
		getAgesData()
	elif choice == '4':
		getDeviationsReport()

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

def runTheCrunch():
	print ""
	sys.stdout.write("Enter name of database: ")
	databaseName = raw_input()
	sys.stdout.write("Output file: ")
	outputFile = raw_input()
	sys.stdout = open(outputFile, 'w')
	thecrunch.theCrunch(databaseName)
	sys.stdout.close()
	exit()
	
def getAgesData():
	print ""
	sys.stdout.write("Enter name of database: ")
	databaseName = raw_input()
	sys.stdout.write("Output file: ")
	outputFile = raw_input()
	sys.stdout = open(outputFile, 'w')
	ages.generateAgesReport(databaseName)
	sys.stdout.close()
	exit()

def getDeviationsReport():
	print ""
	
	sys.stdout.write("Enter deiviation threshold (% points off norm): ")
	deviationThreshold = int(raw_input())
	
	sys.stdout.write("Enter minimum respondents: ")
	minimumRespondents = int(raw_input())
	
	sys.stdout.write("Enter database name: ")
	databaseName = raw_input()
	sys.stdout.write("Output file: ")
	outputFile = raw_input()
	print "Generating report, writing to " + outputFile
	sys.stdout = open(outputFile, 'w')
	correlations.generateReport(deviationThreshold, minimumRespondents, databaseName)
	sys.stdout.close()
	exit()


printMenu()
