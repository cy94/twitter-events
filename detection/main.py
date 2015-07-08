import statistics
import stddev
import fileio

def idf_stddev():
	start_date = raw_input("Enter start date, time (yyyy-mm-dd hh:MM): ")
	end_date = raw_input("Enter finish date, time (yyyy-mm-dd hh:MM): ") 

	word_stdev = stddev.get_word_stdev(start_date, end_date)

	sorted_stdev = sorted(word_stdev.iteritems(), key=lambda x:x[1], reverse=True)
	fileio.write_to_file(sorted_stdev, "out/mh17.csv")

	statistics.print_stats(word_stdev, 0.8, 0.3)
	statistics.plot_stats(word_stdev)

def idf():
	start_date = raw_input("Enter start date, time (yyyy-mm-dd hh:MM): ")
	end_date = raw_input("Enter finish date, time (yyyy-mm-dd hh:MM): ") 

	word_idf = stddev.get_word_IDFcomplete(start_date, end_date)

def main():
	idf_stddev()
	# idf()

if __name__ == '__main__':
	main()