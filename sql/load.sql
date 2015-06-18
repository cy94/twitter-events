-- load.sql

-- Initial version of CSV to MySQL script
-- Use scripts/load.sh instead to import a batch of CSV files

-- inserts twitter feed data into the table tweet
-- the first line contains the column names
LOAD DATA LOCAL INFILE 
	'~/Desktop/internship/data/qz8501/cut/2014_12_28_01.csv' 
INTO TABLE 
	tweet 
IGNORE 1 LINES
	(id, @date_var, content)
SET
	creation_date = STR_TO_DATE(@date_var, '%a %b %e %k:%i:%s GMT %Y')
	;