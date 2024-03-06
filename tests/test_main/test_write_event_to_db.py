import pytest
import sqlite3
from datetime import datetime
from cli_chronicler.main import TimePunchEvent, build_tables


def test_write_event_to_db(tmpdir):
    db_path = tmpdir.join("test_db.db")
    conn = sqlite3.connect(db_path)
    build_tables(conn)

    event_time_utc = datetime.utcnow()
    event_time_local = datetime.now()
    description = "test time punch event"
    event = TimePunchEvent(event_time_utc, event_time_local, description)
    event.write_event_to_db(conn)

    with conn:
        res = conn.execute("select * from time_punch_events;")
        records = res.fetchall()

    assert records == [
        (
            event_time_utc.strftime("%Y-%m-%d %H:%M:%S.%f"),
            event_time_local.strftime("%Y-%m-%d %H:%M:%S.%f"),
            description,
        )
    ]
