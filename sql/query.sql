-- convert the date from string to MySQL date format
-- and select tweets with the required content 
-- eg - 'quake'

create TEMPORARY TABLE formatted as (
	select STR_TO_DATE(creation_date, '%a %b %e %k:%i:%s GMT %Y') as cdate 
	from nepal_quake
	where LOWER(content) like '%quake%' 
);

-- select only the hour and minute from the date field
create TEMPORARY TABLE minutes as ( 
		select DATE_FORMAT(cdate, '%H:%i') as minute 
		from formatted
	);

-- group by minute to get the tweets/minute rate
drop table if exists rate;
create TABLE rate
	as (
		select
			minute, 
			count(*) as num_tweets	
		from
			minutes
		group by
			minute
	);

-----------------------
-- better version - all of above in one query, no temp tables

-- select rows with required keyword
-- group by (hour, minute)
-- output time has only minute and hour
-- output has count of each group
select
	TIME(creation_date) as time,
	COUNT(*) as count
from tweet 
where
	LOWER(content) like '%quake%'
group by 
	HOUR(creation_date), MINUTE(creation_date)
	;

