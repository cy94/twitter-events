import statistics
import stddev
import fileio

def idf_stddev():
	start_date = raw_input("Enter start date, time (yyyy-mm-dd hh:MM): ")
	end_date = raw_input("Enter finish date, time (yyyy-mm-dd hh:MM): ") 

	word_stdev = stddev.get_word_stdev(start_date, end_date)

	sorted_stdev = sorted(word_stdev.iteritems(), key=lambda x:x[1], reverse=True)
	statistics.print_stats(word_stdev, 0.8, 0.3)

	fileio.write_stddev_to_file(sorted_stdev, "out/mh17.csv")

	statistics.plot_stats(word_stdev)


def idf():
	start_date = raw_input("Enter start date, time (yyyy-mm-dd hh:MM): ")
	end_date = raw_input("Enter finish date, time (yyyy-mm-dd hh:MM): ") 

	word_stddev, word_idf = stddev.get_word_IDFcomplete(start_date, end_date, True, 0.7)

	sorted_stdev = sorted(word_stddev.iteritems(), key=lambda x:x[1], reverse=True)
	statistics.print_stats(word_stddev, 0.7, 0.3)

	fileio.write_stddev_to_file(sorted_stdev, "out/mh17sd.csv")
	fileio.write_idf_to_file(word_idf, "out/mh17.csv")

	statistics.plot_stats(word_stddev)


def main():
	# idf_stddev()
	idf()

if __name__ == '__main__':
	main()