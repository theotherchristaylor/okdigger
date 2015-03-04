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


def getQuestionDeviation(question_id, pivot_question_id, output = False):

	greatestDeviation = 0

	#Add number of respondents
	if True:
	#if getNumberOfRespondents(question_id) > minimumRespondents and getNumberOfRespondents(pivot_question_id) > minimumRespondents:
		#sampleSize = str(getNumberOfRespondents(question_id))
		
		pivot_question = getQuestionPercentages(pivot_question_id)
		question = getQuestionPercentages(question_id)
	
		pivot_question_text = pivot_question.keys()[0]
		question_text = question.keys()[0]

		pivot_question_answers = pivot_question.values()[0]
		question_answers = question.values()[0]
		
		greatestDeviation = 0

		if output:
			print ""
			print "OVERALL ANSWERS:"
			#print ""
			#print "Number of respondents: " + str(sampleSize)
			print ""
			print 'Pivot question: ' + str(pivot_question_id) + ' "' + pivot_question_text + '"'
			for (answer, percentage) in pivot_question_answers.items():
				print "  " + answer + " " + str(percentage) + "%"
			print ""
			print "Question: " + str(question_id) + ' "' + question_text + '" '
			for (answer, percentage) in question_answers.items():
				print "  " + answer + " " + str(percentage) + "%"
			print ""
			print "---------------------"
			print ""
			print "CROSS REFERENCED ANSWERS"
			print ""


		for answer in pivot_question_answers.keys():
			if getNumberOfRespondents(pivot_question_id, answer) > minimumRespondents:
				if output:
					print str(pivot_question_id) + ' Response: "' + pivot_question_text + '" ' + answer
					print str(question_id) + ' Response: "' + question_text + '" '
					print ""
					print 'Responents: ' + str(getNumberOfRespondents(question_id, answer))
					print ""
				cross_referenced = getQuestionWithPivot(question_id, pivot_question_id, answer)
				cross_referenced_answers = cross_referenced.values()[0]
				for (text, percentage) in cross_referenced_answers.items():
					deviation = abs(cross_referenced_answers[text] - question_answers[text])
					if deviation > greatestDeviation:
						greatestDeviation = deviation
					if output: print text + " " + str(percentage) + "% (" + str(deviation) + " point deviation)"
				if output: print "-------"
			#print "Greatest deviation = " + str(greatestDeviation)
			if output: print "Greatest deviation = " + str(greatestDeviation)
			return greatestDeviation
		else:
			print "Too few respondents."
			return 0
	
	else:
		return 0

#def getNumberOfRespondents(question_id):
#	query = 'select count("' + str(question_id) + '") from Answers'
#	numAnswers = db.executeQuery(query, 'fetchone')
#	return int(str(numAnswers)[1:-2])

def getNumberOfRespondents(question_id, answer):
	query = 'select count("' + str(question_id) + '") from Answers where "' + str(question_id) + '"="' + answer + '"'
	numAnswers = db.executeQuery(query, 'fetchone')
	
	return int(str(numAnswers)[1:-2])


def getNumberOfQuestions():
	query = 'select count(question_id) from Questions'
	numQuestions = db.executeQuery(query, 'fetchone')
	return int(str(numQuestions)[1:-2])



deviationThreshold = 30 # Only print questions with 50% deviation or greater
minimumRespondents = 50 # Must have at least 200 respondents

totalQuestions = getNumberOfQuestions()

print "Total questions: " + str(totalQuestions)

#for pivot_question in range(1, totalQuestions + 1):
for pivot_question in range(386, 511):
	for question in range(1, totalQuestions + 1):
		if pivot_question != question:	
			deviation = getQuestionDeviation(question, pivot_question)
	
			if deviation >= deviationThreshold:
				print "############################################################\n"
				print "Pivot question " + str(pivot_question) + " and question " + str(question) + " have deviation of " + str(deviation) + "%"
				getQuestionDeviation(question, pivot_question, True)
				print ""

