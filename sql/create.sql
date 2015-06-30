-- create.sql

-- creates the tweet table for twitter data
-- contains the first 3 columns - tweet ID, date and time, content

drop table if exists tweet;

create table tweet ( 
	id BIGINT(20) UNSIGNED, 
	creation_date DATETIME,
	content VARCHAR(150) 
	);