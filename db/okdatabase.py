import sqlite3 as lite

# Always use 'with' keyword in methods that make queries 

class OKDatabase:
	
	def __init__(self, databaseName):
		self.databaseName = databaseName
		self.con = lite.connect(self.databaseName)

	def initDatabase(self):
		query = "CREATE TABLE Details(id TEXT, Last_Online TEXT, Orientation TEXT, Ethnicity TEXT, Height TEXT, Body_Type TEXT, Diet TEXT, Smoking TEXT, Drinking TEXT, Drugs TEXT, Religion TEXT, Relationship TEXT, Sign TEXT, Education TEXT, Job TEXT, Income TEXT, Offspring TEXT, Pets TEXT, Speaks TEXT)"

		with self.con:
			cur = self.con.cursor()			
			cur.execute(query)
		
	def dropTable(self, tableName):
		query = "DROP TABLE IF EXISTS " + tableName

		with self.con:
			cur = self.con.cursor()
			cur.execute(query)

	def addUserDetails(self, user, detailsDict):
		with self.con:
			cur = self.con.cursor()
			cur.execute("INSERT INTO Details VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
				(user,
				detailsDict['Last Online'],
				detailsDict['Orientation'],
				detailsDict['Ethnicity'],
				detailsDict['Height'],
				detailsDict['Body Type'],
				detailsDict['Diet'],
				detailsDict['Smoking'],
				detailsDict['Drinking'],
				detailsDict['Drugs'],
				detailsDict['Religion'],
				detailsDict['Relationship'],
				detailsDict['Sign'],
				detailsDict['Education'],
				detailsDict['Job'],
				detailsDict['Income'],
				detailsDict['Offspring'],
				detailsDict['Pets'],
				detailsDict['Speaks'])
			)

