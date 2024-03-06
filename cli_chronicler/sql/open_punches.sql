-- open punches
select
	time_punched_at_local
  , coalesce(description, 'day start') as description
from (select
			time_punched_at_local
		  , description
		  , count(*) over (partition by description order by time_punched_at_local) % 2 as is_odd
		  , lead(time_punched_at_local, 1) over (partition by description order by time_punched_at_local) as description_lead
		from time_punch_events) as events_with_windows
where is_odd = 1
  and description_lead is null;
