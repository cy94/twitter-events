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

def get_stopwords(fname):
	with open(fname, 'r') as f:
		return set(f.readlines())

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
	
	english_chars = set(string.printable)

	word_IDFseries = {}
	trans_table = dict((ord(char), unicode(" ", "utf-8")) for char in string.punctuation)

	for time, tweets in grouped_tweets.iteritems():
		word_count_dict = {}

		# remove apostrophe
		tweet_text = " ".join(tweets).replace("'", "").lower()
		# tweet_text = " ".join(tweets).lower()

		# replace other punctuation with space
		tweet_text = tweet_text.translate(trans_table)
		
		# then tokenize on whitespace
		words = tweet_text.split()

		# remove stopwords
		words = [w for w in words if w not in STOPWORDS]

		# checks if a word has non english (non printable) chars
		is_english = lambda word : not set(word) - english_chars

		# remove words with non printable chars 
		words = filter(is_english, words)

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

def get_word_stdev_from_IDFseries(word_IDFseries):
	word_stdev = {}

	print "Finding stdevs"
	for word in word_IDFseries:
		word_stdev[word] = numpy.std(word_IDFseries[word])

	return word_stdev

def get_word_stdev(start_date, end_date):
	cnx, cursor = init_db()

	print "Getting data"
	cursor = get_data_by_date(cursor, start_date, end_date)

	# group tweets by time (minute)
	grouped_tweets = group_tweets_by_time(cursor)
	
	# count tweets per minute
	tweets_per_minute_dict = {
		time : len(tweets) for (time, tweets) in grouped_tweets.iteritems()
	}

	word_IDFseries = get_word_IDFseries(grouped_tweets, tweets_per_minute_dict)		

	print "Unique words: ", len(word_IDFseries)

	# dict for word - std dev of word IDF in this time period
	word_stdev = get_word_stdev_from_IDFseries(word_IDFseries)
	
	close_db(cnx)

	return word_stdev	

def main():
	pass	

if __name__ == '__main__':
	main()
