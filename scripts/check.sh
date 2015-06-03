# check for keyword before putting in database
# $1 is the keyword from command line

if [ $# -eq 0 ]; then
	#statements
	echo "usage: ./check <keyword>"
	exit -1
fi

echo Searching for $1

for f in *.csv; do
	echo checking $f
	cat $f | grep -i $1 | wc -l
done	