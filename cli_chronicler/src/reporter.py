import sqlite3

DB_FILE_PATH = ".chronicler/punch_db.db"
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
		from time_punch_events) as events_with_windows
where is_odd = 1
  and description_lead is null;
"""


def generate_daily_report():
    conn = sqlite3.connect(DB_FILE_PATH)
    with conn:
        result = conn.execute(HOURS_BY_CATEGORY).fetchall()
    width = 40
    print("Hour Totals by Category")
    for row in result:
        print(row[0].ljust(width) + str(row[1]).ljust(width))


def retrieve_open_punches():
    conn = sqlite3.connect(DB_FILE_PATH)
    with conn:
        result = conn.execute(OPEN_PUNCHES).fetchall()
    width = 20
    print("Open Punches")
    for row in result:
        print(row[1].ljust(width) + str(row[0]).ljust(width))
