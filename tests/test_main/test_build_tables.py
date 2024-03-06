import pytest
import sqlite3
from cli_chronicler.main import build_tables
import logging


def test_build_tables(tmpdir):
    db_path = tmpdir.join("test_db.db")
    logging.info(db_path)
    conn = sqlite3.connect(db_path)
    build_tables(conn)

    with conn:
        res = conn.execute("select name from sqlite_master where type = 'table';")
        tables = res.fetchall()

    assert tables == [("time_punch_events",)]

    with conn:
        res = conn.execute("pragma table_info('time_punch_events');")
        columns = [(row[1], row[2]) for row in res.fetchall()]

    assert columns == [
        ("time_punched_at_utc", "TEXT"),
        ("time_punched_at_local", "TEXT"),
        ("description", "TEXT"),
    ]
