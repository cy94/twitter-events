
import numpy
import matplotlib.pyplot as plt

def print_stats(word_stdev, IDF_HIGH, IDF_LOW):
	total = float(len(word_stdev.keys()))

	less4 = len([word for word in word_stdev.keys()   if len(word) <= 4])
	great10 = len([word for word in word_stdev.keys() if len(word) >= 10])

	highidf = len([idf for idf in word_stdev.values() if idf > IDF_HIGH])
	lowidf = len([idf for idf in word_stdev.values()  if idf < IDF_LOW])

	print "%f" % (less4/total)
	print "%f" % (great10/total)
	print "%f" %(highidf/total)
	print "%f" %(lowidf/total)

def plot_stats(word_stdev):
	plt.hist(word_stdev.values(), normed=True, bins=50)
	plt.title("IDF Std-dev histogram")
	plt.xlabel("IDF Std-dev")
	plt.ylabel("Count")
	plt.show()

	