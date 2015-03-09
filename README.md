##OKDigger - a python tool for grabbing okcupid data. 
This project contains a set of tools that can scrape okcupid data and archive it in a simple sqlite3 database. This data can then be explored to reveal correlations and trends. I built it because I love [OKTrends](http://blog.okcupid.com/), and I wanted to be able to mine the data myself. 
##Overview
The project consists of two main files:

* #####okdigger.py
This file contains the class OKDigger, which implements the methods that connect to and communicate with the okcupid site. The methods that do the actual scraping are in here. They include:
	* login()
	* quickmatch()
	* getProfile(user)
	* getUsernames(num_usernames, [output])
	* getUserDetails(user, [output])
	* getUserAnswers(user, [output])
	* setSearchParams(search_type)

* #####okdatabase.py
	This file contains the class OKDatabase, which implements the methods that connect to and communicate with a local sqlite3 database. The methods that achive the scraped data are in here. They include:
	* initDatabase()
	* destroyDatabase()
	* addUserDetails(user, detailsDict, [output])
	* addUserAnswers(user, answers, [output])

The file that uses these tools is called freelance_sociology.py. It contains a guided menu that will help build the database and generate reports. Start here. 

##Usage/Installation

To install sqlite3, run `sudo apt-get install sqlite3 libsqlite3-dev`

To install dependencies, run
`sudo pip install -r requirements.txt`

To get started, create a file called _config.txt_ with has a single line consisting of valid okcupid credentials in the form `username:password`. 

Next, run `python freelance_sociology.py`. Start with option 5, "Generate config.txt". Enter your username and password. 

Next, build the database using a given search. Once the database is built, you can use the data to generate reports on user age, details, and question deviations. 

_**Note:** In order to see the answered questions of other users, the account that you connect with must have answered the same questions as the other user. So in order to get the most data, get a profile and start answering those questions!_

##Database

The database consists of three tables:
* _Details_ - Contains user details, id is user name. 
* _Questions_ - Contains the questions text, id is autoincremented question_id.
* _Answers_ - Contains user answers to questions. Columns are question_id and primary id is user name.

##License:

Released under GPL 3.0, or beerware, or whatever, it doesn't matter, it's a tool to scrape another website's data. Don't be a jerk.

