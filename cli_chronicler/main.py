import argparse
from datetime import datetime
import sqlite3
import os
from cli_chronicler.src.reporter import generate_daily_report, retrieve_open_punches

# Global Constants
DB_FILE_PATH = "cli_chronicler/db/punch_db.db"
SQL_FILE_PATH = "cli_chronicler/sql/time_punch_events.sql"


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


def build_tables(sql_file_path, conn):
    with open(sql_file_path) as f:
        for statement in f.read().split("\n\n"):
            conn.execute(statement)


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
            conn = sqlite3.connect(DB_FILE_PATH)
            build_tables(SQL_FILE_PATH, conn)
            punch_to_log.write_event_to_db(conn)


if __name__ == "__main__":
    main()
