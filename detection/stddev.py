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

import string
import nltk

def get_stopwords(fname):
	with open(fname, 'r') as f:
		return f.readlines()

STOPWORDS = get_stopwords("stopwords.txt")


def init_db():
	cnx = mysql.connector.connect(user='root', password='internship',
                              host='127.0.0.1',
                              database='twitter')

	cursor = cnx.cursor()

	return cnx, cursor

def close_db(cnx):
	cnx.close()	

def get_data_by_date(cursor, start_date, end_date):
	query = "select creation_date, content from tweet_en where creation_date between '{0}' and '{1}'"
	query = query.format(start_date, end_date)

	cursor.execute(query)

	return cursor

def get_idf(total, count):
	return math.log(float(total)/(count + 1))	

def group_tweets_by_time(cursor):
	grouped_tweets = {}

	for (date, tweet) in cursor:
		# remove the second, microsecond parts from the time 
		time = date.replace(second=0, microsecond=0).time()

		if time in grouped_tweets:
			grouped_tweets[time].append(tweet)
		else:
			grouped_tweets[time] = [tweet]

	return grouped_tweets

# count occurrences of words per minute and find IDF
def get_word_IDFseries(grouped_tweets, tweets_per_minute_dict):
	print "Finding IDFs"
	
	word_IDFseries = {}

	for time, tweets in grouped_tweets.iteritems():
		word_count_dict = {}

		tweet_text = " ".join(tweets)
		
		# remove apostrophe
		# replace other punctuation with a whitespace
		# then tokenize on whitespace
		words = tweet_text.replace("'", "").translate(None, string.punctuation).split()
		words = [w for w in words if w not in STOPWORDS]

		for word in words:
			if word in word_count_dict:
				word_count_dict[word] += 1
			else:
				word_count_dict[word]  = 1

		# find IDF for each word in this minute
		for word in word_count_dict:
			idf = get_idf(tweets_per_minute_dict[time], word_count_dict[word])

			if word not in word_IDFseries:
				# create a list
				word_IDFseries[word] = [idf]
			else:	
				# append to list
				word_IDFseries[word].append(idf)

	return word_IDFseries

def write_to_file(word_stdev):
	print "Writing to file"

	with open("stdev.out", "w") as f:
		for w, c in word_stdev:
			s = w + ", " + str(c) + "\n"
			s = s.encode("utf8")
			f.write(s)

def get_word_stdev_from_IDFseries(word_IDFseries):
	word_stdev = {}

	print "Finding stdevs"
	for word in word_IDFseries:
		# data series is stored as array in word_stdev
		word_stdev[word] = numpy.std(word_IDFseries[word])

	return word_stdev
		
def main():
	cnx, cursor = init_db()

	start_date = raw_input("Enter start date, time (yyyy-mm-dd hh:MM): ")
	end_date = raw_input("Enter finish date, time (yyyy-mm-dd hh:MM): ") 

	print "Getting data"
	cursor = get_data_by_date(cursor, start_date, end_date)

	# group tweets by time (minute)
	grouped_tweets = group_tweets_by_time(cursor)
	
	tweets_per_minute_dict = {
		time : len(tweets) for (time, tweets) in grouped_tweets.iteritems()
	}

	word_IDFseries = get_word_IDFseries(grouped_tweets, tweets_per_minute_dict)		

	print "Unique words: ", len(word_IDFseries)

	# dict for word - std dev of word IDF in this time period
	word_stdev = get_word_stdev_from_IDFseries(word_IDFseries)
	sorted_stdev = sorted(word_stdev.iteritems(), key=lambda x:x[1], reverse=True)

	write_to_file(sorted_stdev)
	close_db(cnx)	

if __name__ == '__main__':
	main()
