-- hours by category
select
	coalesce(description, 'total time at work') as description
  , round(sum(time_hours), 4) as hours
from (select
		    time_punched_at_local
		  , (julianday(time_punched_at_local) - lag(julianday(time_punched_at_local), 1) over (partition by description)) * 24 as time_hours
		  , description
		from time_punch_events
		where substr(time_punched_at_utc, 1, 10) = current_date) as time_elapsed
where time_hours is not null
group by description
order by hours desc;
