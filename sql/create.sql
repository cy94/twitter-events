drop table if exists tweet;

-- the tweet table stores the tweet creation date+time
-- and the text of the tweet
create table tweet ( 
	id INT(20), 
	creation_date DATETIME,
	content VARCHAR(150) 
	);