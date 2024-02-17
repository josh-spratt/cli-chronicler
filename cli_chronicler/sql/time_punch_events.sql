drop table if exists time_punch_events;

create table if not exists time_punch_events (
    time_punched_at_utc text,
    time_punched_at_local text,
    description text
);
