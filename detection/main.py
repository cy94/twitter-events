import statistics
import stddev
import fileio

def main():
	start_date = raw_input("Enter start date, time (yyyy-mm-dd hh:MM): ")
	end_date = raw_input("Enter finish date, time (yyyy-mm-dd hh:MM): ") 

	word_stdev = stddev.get_word_stdev(start_date, end_date)

	sorted_stdev = sorted(word_stdev.iteritems(), key=lambda x:x[1], reverse=True)
	fileio.write_to_file(sorted_stdev, "out/quake.csv")

	# statistics.print_stats(word_stdev, 1.8, 0.3)
	statistics.plot_stats(word_stdev)

if __name__ == '__main__':
	main()