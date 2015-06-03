# select first 3 columns in a list of CSV files
# and store in the cut directory with the same filename

# This script is not required! MySQL LOAD DATA discards
# the remaining columns when only the first 3 columns are
# specified 

for f in *.csv; do
	#statements
	echo cutting $f
	cat $f | cut -d$'\t' -f1-3 > ../cut/$f
	echo finished $f
done