
# unzip .zip files from the TweetData directory to 
# a destination directory 

# prefix: The prefix of the file series to be extracted
# 		eg: 2015_05_12
# start: The start hour of file series (0-23)
# end:   End hour
# destination: Directory in which zip files are extracted


if (( $# < 4 )); then
	#statements
	echo "usage: ./check <prefix> <start> <end> <destination>"
	exit -1
fi

prefix=$1
start=$2
end=$3
destination=$4

echo "Prefix      : $prefix"
echo "Start       : $start"
echo "End         : $end"
echo "Destination : $destination"

for n in `seq -w $start $end`; do 
	fname=$prefix$n

	echo "Unzipping $fname"

	unzip -d $destination $fname
done