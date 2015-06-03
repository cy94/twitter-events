# mysql LOAD INFILE from command line

# loads all the CSV files in the pwd into the MySQL database
# db: twitter
# username: root
# password: internship
# table: tweet

# ignores the first line (header)
# then converts the second column (date) to a 
# MySQL date

for f in *.csv
do
	printf "Loading $f ..."
    mysql -e "LOAD DATA LOCAL INFILE '`pwd`/$f' INTO TABLE tweet IGNORE 1 LINES (id, @date_var, content) SET creation_date = STR_TO_DATE(@date_var, '%a %b %e %k:%i:%s GMT %Y')	;" -u root --password=internship twitter
    printf "done\n"

done