import argparse
from datetime import datetime
import os
from cli_chronicler.src.reporter import (
    generate_daily_report,
    retrieve_open_punches,
    connect_to_db,
)
from cli_chronicler.src.utils import read_config
import logging


class TimePunchEvent:
    """Class for keeping track of a time punch event."""

    def __init__(self, time_punched_at_utc, time_punched_at_local, description=None):
        self.time_punched_at_utc = time_punched_at_utc
        self.time_punched_at_local = time_punched_at_local
        self.description = description

    def write_event_to_db(self, conn):
        """Writes time punch event to sqlite db."""
        logger = logging.getLogger(__name__)  # Get logger for current module
        with conn:
            conn.execute(
                "insert into time_punch_events (time_punched_at_utc, time_punched_at_local, description) values (?, ?, ?)",
                (
                    self.time_punched_at_utc,
                    self.time_punched_at_local,
                    self.description,
                ),
            )
        logger.info("Successfully wrote time punch event to DB.")


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
    script_dir = os.path.dirname(__file__)
    config_path = os.path.join(script_dir, "config.yaml")
    config = read_config(config_path)
    db_file_path = config["db_file_path"]
    report_sql_path = os.path.join(script_dir, config["report_sql_path"])
    open_punch_sql_path = os.path.join(script_dir, config["open_punch_sql_path"])

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--description", required=False)
    parser.add_argument("-r", "--report", required=False, action="store_true")
    parser.add_argument("-o", "--open", required=False, action="store_true")
    arguments = parser.parse_args()

    if os.path.isfile(db_file_path):
        conn = connect_to_db(db_file_path)
        if arguments.report:
            generate_daily_report(conn, report_sql_path)
        elif arguments.open:
            retrieve_open_punches(conn, open_punch_sql_path)
        else:
            punch_to_log = TimePunchEvent(
                datetime.utcnow(), datetime.now(), arguments.description
            )
            punch_to_log.write_event_to_db(conn)
    else:
        os.mkdir(".chronicler")
        conn = connect_to_db(db_file_path)
        build_tables(conn)
        if arguments.report:
            generate_daily_report(conn, report_sql_path)
        elif arguments.open:
            retrieve_open_punches(conn, open_punch_sql_path)
        else:
            punch_to_log = TimePunchEvent(
                datetime.utcnow(), datetime.now(), arguments.description
            )
            punch_to_log.write_event_to_db(conn)


if __name__ == "__main__":
    main()
