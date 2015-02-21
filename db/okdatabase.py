import sqlite3 as lite

# Always use 'with' keyword in methods that make queries 


class OKDatabase:
	
	def __init__(self, databaseName):
		self.databaseName = databaseName
		self.con = lite.connect(self.databaseName)

	def initDatabase(self):

		with self.con:
			cur = self.con.cursor()			

			query = "CREATE TABLE Details(id TEXT, Last_Online TEXT, Orientation TEXT, Ethnicity TEXT, Height TEXT, Body_Type TEXT, Diet TEXT, Smoking TEXT, Drinking TEXT, Drugs TEXT, Religion TEXT, Relationship TEXT, Sign TEXT, Education TEXT, Job TEXT, Income TEXT, Offspring TEXT, Pets TEXT, Speaks TEXT)"
			
			try:
				cur.execute(query)
			except:
				pass

			query = "CREATE TABLE Questions(question_id INTEGER PRIMARY KEY AUTOINCREMENT, question_text TEXT)"

			try:
				cur.execute(query)
			except:
				pass
			
			query = "CREATE TABLE Answers(id TEXT)"

			try:
				cur.execute(query)
			except:
				pass
		
	def dropTable(self, tableName):
		query = "DROP TABLE IF EXISTS " + tableName

		with self.con:
			cur = self.con.cursor()
			cur.execute(query)

	def destroyDatabase(self):
		self.dropTable('Details')
		self.dropTable('Answers')
		self.dropTable('Questions')
	
	def addUserDetails(self, user, detailsDict, output = False):
		if output:
			print "[+] Adding details to database for user " + user
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

	def checkAddQuestion(self, question):
		question = self.sanitizeQuotes(question)

		with self.con:
			cur = self.con.cursor()
			
			# Make sure we have question in Questions table
			# May have an ERROR here
			try:
				query = "SELECT * FROM Questions WHERE question_text='" + question + "'"
				cur.execute(query)
				rows = cur.fetchone()
			except Exception, e:
				print "Error with query."
				print query

			if rows:
				question_id = rows[0]
				#print "FOUND QUESTION WITH ID " + str(question_id)
				return int(str(question_id))

			# Question is not in Questions table, add it 
			else:			
				#print "No question " + question + " found." 
				query = 'INSERT INTO Questions (question_text) VALUES ("' + question + '")'
				cur.execute(query)
				question_id = cur.lastrowid
				#print "Inserted question at id " + str(question_id)
				return int(question_id)
	
	def checkAddUserInAnswers(self, user):
		with self.con:
			cur = self.con.cursor()
			query = 'SELECT * FROM Answers WHERE id="' + user + '"'
			cur.execute(query)

			if cur.fetchall():
				#print "Found user " + user + " in Answers."
				return True
			else:
				query = 'INSERT INTO Answers (id) VALUES ("' + user + '")'
				cur.execute(query)
				#print "Inserted user " + user + " in Answers."
				return True
				
	def checkAddQuestionInAnswers(self, user, question_id, answer):
		found = False
		answer = self.sanitizeQuotes(answer)

		with self.con:
			cur = self.con.cursor()
			# Make sure question is in Answers table by question_id
			query = "PRAGMA table_info('Answers')"
			cur.execute(query)
			columns = cur.fetchall()
			for column in columns:
				if str(column[1]) == str(question_id):
					found = True
					#print "Found question_id"
					
			if  not found:
				# Add column
				query = 'ALTER TABLE Answers ADD COLUMN "' + str(question_id) + '" INTEGER'
				cur.execute(query)
				#print "Added column for question id."
		
			# Add answer under column
			query = 'UPDATE Answers SET "' + str(question_id) + '"="' + answer + '" WHERE id="' + user + '"'
			cur.execute(query)
			#print "Updated question_id column with answer."

	def addUserAnswers(self, user, answers, output = False):
		
		if output:
			print "[+] Adding answers to database for user " + user
		self.checkAddUserInAnswers(user)
		for (question, answer) in answers.items():
			question_id = self.checkAddQuestion(question)
			self.checkAddQuestionInAnswers(user, question_id, answer)
	
	def sanitizeQuotes(self, s):
		s = s.replace('"', '')
		s = s.replace("'", "")
		return s

	def checkUserExists(self, user, output=False):
		with self.con:
			cur = self.con.cursor()
			query = 'SELECT id FROM Details'
			cur.execute(query)
			user_list = cur.fetchall()
			for item in user_list:
				#print "Making sure " + str(item)[3:-3] + " != " + str(user)
				if str(item)[3:-3] == str(user):
					if output:
						print "[-] User " + user + " already in database"
					return 1
			return 0
					
