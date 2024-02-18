import sqlite3

DB_FILE_PATH = "cli_chronicler/db/punch_db.db"
HOURS_BY_CATEGORY = """
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
"""
OPEN_PUNCHES = """
-- open punches
select
	time_punched_at_local
  , description
from (select
			time_punched_at_local
		  , description
		  , count(*) over (partition by description order by time_punched_at_local) % 2 as is_odd
		  , lead(time_punched_at_local, 1) over (partition by description order by time_punched_at_local) as description_lead
		from time_punch_events
		where substr(time_punched_at_utc, 1, 10) = current_date) as events_with_windows
where is_odd = 1
  and description_lead is null;
"""


def generate_daily_report():
    conn = sqlite3.connect(DB_FILE_PATH)
    with conn:
        result = conn.execute(HOURS_BY_CATEGORY).fetchall()
    width = 40
    print("+=" + "=" * 46 + "=+")
    print("Hour Totals by Category")
    print("+=" + "=" * 46 + "=+")
    for row in result:
        print(row[0].ljust(width) + str(row[1]).ljust(width))
    print("+=" + "=" * 46 + "=+")
