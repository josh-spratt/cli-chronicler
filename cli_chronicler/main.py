import argparse
from datetime import datetime
import sqlite3
import os
from cli_chronicler.src.reporter import generate_daily_report, retrieve_open_punches

# Global Constants
DB_FILE_PATH = ".chronicler/punch_db.db"

class TimePunchEvent:
    """Class for keeping track of a time punch event."""

    def __init__(self, time_punched_at_utc, time_punched_at_local, description=None):
        self.time_punched_at_utc = time_punched_at_utc
        self.time_punched_at_local = time_punched_at_local
        self.description = description

    def write_event_to_db(self, conn):
        """Writes time punch event to sqlite db."""
        with conn:
            conn.execute(
                "insert into time_punch_events (time_punched_at_utc, time_punched_at_local, description) values (?, ?, ?)",
                (
                    self.time_punched_at_utc,
                    self.time_punched_at_local,
                    self.description,
                ),
            )


def build_tables(conn):
    with conn:
        conn.execute(
            """
create table if not exists time_punch_events (
    time_punched_at_utc text,
    time_punched_at_local text,
    description text
);"""
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--description", required=False)
    parser.add_argument("-r", "--report", required=False, action="store_true")
    parser.add_argument("-o", "--open", required=False, action="store_true")
    arguments = parser.parse_args()
    if arguments.report:
        generate_daily_report()
    elif arguments.open:
        retrieve_open_punches()
    else:
        punch_to_log = TimePunchEvent(
            datetime.utcnow(), datetime.now(), arguments.description
        )
        if os.path.isfile(
            DB_FILE_PATH
        ):  # If the db file already exists with punches, then insert.
            conn = sqlite3.connect(DB_FILE_PATH)
            punch_to_log.write_event_to_db(conn)
        else:  # If the db file does not exist, then create new file, create tables, and insert.
            os.mkdir(".chronicler")
            conn = sqlite3.connect(DB_FILE_PATH)
            build_tables(conn)
            punch_to_log.write_event_to_db(conn)


if __name__ == "__main__":
    main()
