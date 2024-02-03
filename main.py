import argparse
from datetime import datetime
import csv
import os

HEADER = ["time_punched_at", "project"]
PATH_TO_CSV = "out/punches.csv"


class TimePunchEvent:
    """Class for keeping track of a time punch event."""

    def __init__(self, time_punched_at, project=None):
        self.time_punched_at = time_punched_at
        self.project = project

    def write_event_to_new_csv(self):
        with open(PATH_TO_CSV, "w") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(HEADER)
            writer.writerow([self.time_punched_at.isoformat(), self.project])

    def append_event_to_csv(self):
        with open(PATH_TO_CSV, "a") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([self.time_punched_at.isoformat(), self.project])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project", required=False)
    arguments = parser.parse_args()
    punch_to_log = TimePunchEvent(datetime.utcnow(), arguments.project)
    if os.path.isfile(PATH_TO_CSV):
        punch_to_log.append_event_to_csv()
    else:
        punch_to_log.write_event_to_new_csv()


if __name__ == "__main__":
    main()
