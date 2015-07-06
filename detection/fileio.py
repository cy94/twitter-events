import csv

def csv_to_dict(fname):
	with open(fname, "r") as f:
		reader = csv.reader(f)

		for line in list(reader):
			print line
			
		# return { line[0]: line[1] for line in list(reader) }

def main():
	pass

def write_to_file(word_stdev, fname):
	print "Writing to file"

	with open(fname, "w") as f:
		for w, c in word_stdev:
			s = w + ", " + str(c) + "\n"
			s = s.encode("utf8")
			f.write(s)	

if __name__ == '__main__':
	main()