"""
correlations.py

Pivots off of a single question to find other answers that are outside the standard spread.

Written by Chris Taylor, 2/22/15

"""

from db.okdatabase import OKDatabase

databaseName = "everyone_local.db"
db = OKDatabase(databaseName)

# Define a deviation threshold
	# Scales with number of questions

# Write function that returns deviation for single question

def getQuestionWithPivot(question_id, pivot_question, pivot_answer):
	# Returns question_dict for question_id where user also answered the
	# pivot question with the pivot answer
	results_dict = {}

	# Get the question text
	question_query = 'select question_text from Questions where question_id="%s"' % question_id
	question = db.executeQuery(question_query, 'fetchone')
	question = str(question[0])

	# Build answer_list dict
	answer_list = {}
	answer_query = 'select "%s" from Answers where "%s" is not null and "%s"="%s"' % (question_id, question_id, pivot_question, pivot_answer)
	answers = db.executeQuery(answer_query)
	for answer in answers:
		answer = str(answer[0])
		if answer not in answer_list.keys():
			answer_list[answer] = 1.0
		else:
			answer_list[answer] += 1.0

	total_answers = 0

	# Find total answers
	for answer in answer_list.keys():
		total_answers += answer_list[answer]

	# Replace answer totals with percentages
	for answer in answer_list.keys():
		percentage = int((answer_list[answer] / total_answers) * 100)
		answer_list[answer] = percentage
	
	# Pack into dictionary
	results_dict[question] = answer_list
	return results_dict

def getQuestionPercentages(question_id):
	# Returns question_dict for question_id where user also answered the
	# pivot question with the pivot answer
	results_dict = {}

	# Get the question text
	question_query = 'select question_text from Questions where question_id="%s"' % question_id
	question = db.executeQuery(question_query, 'fetchone')
	question = str(question[0])

	# Build answer_list dict
	answer_list = {}
	answer_query = 'select "%s" from Answers where "%s" is not null' % (question_id, question_id)
	answers = db.executeQuery(answer_query)
	for answer in answers:
		answer = str(answer[0])
		if answer not in answer_list.keys():
			answer_list[answer] = 1.0
		else:
			answer_list[answer] += 1.0

	total_answers = 0

	# Find total answers
	for answer in answer_list.keys():
		total_answers += answer_list[answer]

	# Replace answer totals with percentages
	for answer in answer_list.keys():
		percentage = int((answer_list[answer] / total_answers) * 100)
		answer_list[answer] = percentage
	
	# Pack into dictionary
	results_dict[question] = answer_list
	return results_dict

def getQuestionDeviation(question_id, pivot_question_id):

	#Add number of respondents

	original_question = getQuestionPercentages(question_id)
	pivot_question = getQuestionPercentages(pivot_question_id)
	
	original_answer_percentages = []

	print 'Original question:'
	for question in original_question:
		print question
	for (key, value) in original_question[original_question.keys()[0]].items():
		original_answer_percentages.append(int(value))

	print 'Original answer percentages: ' 
	print original_answer_percentages
	print ""

	print 'Pivot question:'
	for question in pivot_question:
		print question
	for answer in pivot_question[pivot_question.keys()[0]]:
		pivot_answer_percentages = []
		print 'Question answers with pivot answer %s:' % answer
		pivot_answer = getQuestionWithPivot(question_id, pivot_question_id, answer)
		
		for (key, value) in pivot_answer[pivot_answer.keys()[0]].items():
			pivot_answer_percentages.append(int(value))
		print 'Pivot answer percentages: '
		print pivot_answer_percentages
		
		for index in range(0, len(pivot_answer_percentages)):
			diff = abs(original_answer_percentages[index] - pivot_answer_percentages[index])
			print "DEVIATION OF " + str(diff)
		
		print ""

#getQuestionWithPivot(question_id, pivot_question_id, 'No')

getQuestionDeviation(200, 400)
