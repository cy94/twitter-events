#!/usr/bin/python

# stddev.py
# chandan yeshwanth

# a twitter event detection technique that 
# uses std dev threshold to remove stopwords and 
# find keywords

import mysql.connector
import datetime
import math
import numpy

def init_db():
	cnx = mysql.connector.connect(user='root', password='internship',
                              host='127.0.0.1',
                              database='twitter')

	cursor = cnx.cursor()

	return cnx, cursor

def get_data_by_date(cursor, start_date, end_date):
	# query = "select TIME(creation_date), GROUP_CONCAT(content SEPARATOR ' ') from tweet where creation_date between '{0}' and '{1}' limit 10"
	query = "select creation_date, content from tweet_en where creation_date between '{0}' and '{1}'"
	query = query.format(start_date, end_date)

	cursor.execute(query)

	return cursor

def get_idf(total, count):
	return math.log(float(total)/(count + 1))	

def main():
	cnx, cursor = init_db()

	start_date = raw_input("Enter start date, time (yyyy-mm-dd hh:MM): ")
	end_date = raw_input("Enter finish date, time (yyyy-mm-dd hh:MM): ") 

	print "Getting data"
	cursor = get_data_by_date(cursor, start_date, end_date)

	# group tweets by time (minute)
	grouped_tweets = {}

	for (date, tweet) in cursor:
		# remove the second, microsecond parts from the time 
		time = date.replace(second=0, microsecond=0).time()

		if time in grouped_tweets:
			grouped_tweets[time].append(tweet)
		else:
			grouped_tweets[time] = [tweet]

	tweets_per_minute_dict = {
		time : len(tweets) for (time, tweets) in grouped_tweets.iteritems()
	}

	# a dict to store 
	# 	{ time of day (HH:mm) : 
	# 		{
	# 			word1 : IDF in this minute
	#			word2 : ...
	# 		}
	#	  time2 : ...
	# 	}
	# time_wordIDF_dict = {}

	word_stdev = {}

	print "Finding IDFs"
	# count occurrences of words per minute and find IDF
	for time, tweets in grouped_tweets.iteritems():
		wordIDF_dict = {}

		words = " ".join(tweets).lower().split()

		for word in words:
			if word in wordIDF_dict:
				wordIDF_dict[word] += 1
			else:
				wordIDF_dict[word]  = 1

			# initialize with None, fill the std dev of IDF later 
			if word not in word_stdev:
				word_stdev[word] = []

		# find IDF for each word in this minute
		for word in wordIDF_dict:
			# wordIDF_dict[word] = get_idf(tweets_per_minute_dict[time], wordIDF_dict[word])
			# store data series in word_stdev
			word_stdev[word].append(
					get_idf(tweets_per_minute_dict[time], wordIDF_dict[word])
				)

		# add this dict to main dict
		# time_wordIDF_dict[time] = wordIDF_dict

	print "Unique words: ", len(word_stdev)

	print "Finding stdevs"
	for word in word_stdev:
		# data_series = []

		# for time in time_wordIDF_dict:
		# 	# if the word occurred in this time use IDF, else IDF with 0 count
		# 	data_series.append(
		# 		time_wordIDF_dict[time][word] if word in time_wordIDF_dict[time]
		# 		else get_idf(tweets_per_minute_dict[time], 0)
		# 	)

		# word_stdev[word] = numpy.std(data_series)
		# data series is stored as array in word_stdev
		word_stdev[word] = numpy.std(word_stdev[word])

	sorted_stdev = sorted(word_stdev.iteritems(), key=lambda x:x[1], reverse=True)

	print "Writing to file"

	f = open("stdev.out", "w")
	for w, c in sorted_stdev[:100]:
		print w, c
		s = w + ", " + str(c) + "\n"
		s = s.encode("utf8")
		f.write(s)
	f.close()
	
	cnx.close()

if __name__ == '__main__':
	main()
