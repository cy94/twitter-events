-- add an index on the date 
-- the application select tweets in a date range and then
-- searches for keywords
ALTER TABLE tweet ADD INDEX `date_ndx` (`creation_date`);