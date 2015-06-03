
-- create a view to store tweets in a date range
drop view if exists event_tweet;

create view event_tweet as
	select * from tweet
	where 
		creation_date between '2014-12-28 00:00' and '2014-12-29 00:00'
	;