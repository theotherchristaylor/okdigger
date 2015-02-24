""" 
thecrunch.py

An attempt to expose the peculiar behaviours of lonely people. 

Written by Chris Taylor, 2/21/15

"""
from db.okdatabase import OKDatabase

databaseName = "everyone_local.db"

db = OKDatabase(databaseName)
sample_size = db.executeQuery('select count(gender) from Details', 'fetchone')
total_men = db.executeQuery('select count(gender) from Details where gender="Man"', 'fetchone')
total_women = db.executeQuery('select count(gender) from Details where gender="Woman"', 'fetchone')

sample_size = int(sample_size[0])
total_men = int(total_men[0])
total_women = int(total_women[0])

percent_men = float(total_men)/float(sample_size) * 100
percent_women = float(total_women)/float(sample_size) * 100

print """
###################################################
#                                                 #
#                   THE CRUNCH.py                 #
#                                                 #
###################################################
"""

print "%s Lonely souls looking for love.\n" % str(sample_size)

print "%.1f%% Men" % percent_men
print "%.1f%% Women" % percent_women

num_questions = db.executeQuery('select count(question_id) from Questions', 'fetchone')
num_questions = int(num_questions[0])

for index in range(1, num_questions):

	question_id = str(index)
	query = 'select question_text from Questions where question_id="%s"' % question_id
	question = db.executeQuery(query, 'fetchone')
	answer_choices = {}
	query = 'select "%s" from Answers where "%s" is not null' % (question_id, question_id)
	results = db.executeQuery(query)
	print "\nQuestion: %s" % question
	for result in results:
		result = str(result[0])
		if result not in answer_choices.keys():
			answer_choices[result] = 1
		else:
			answer_choices[result] += 1
	
	total_answers = 0

	for (answer, number) in answer_choices.items():
		total_answers += number
	
	for (answer, number) in answer_choices.items():
		percentage = int((float(number)/float(total_answers))*100.0)
		print str(answer) + ": " + str(number) + " (" + str(percentage) + "%)"
