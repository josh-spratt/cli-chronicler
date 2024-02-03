import argparse
from datetime import datetime
import csv
import os

# Global Constants
HEADER = ["time_punched_at", "project"]
PATH_TO_CSV = "out/punches.csv"


class TimePunchEvent:
    """Class for keeping track of a time punch event."""

    def __init__(self, time_punched_at, project=None):
        self.time_punched_at = time_punched_at
        self.project = project

    def write_event_to_new_csv(self):
        """Writes header to new file and time punch event."""
        with open(PATH_TO_CSV, "w") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(HEADER)
            writer.writerow([self.time_punched_at.isoformat(), self.project])

    def append_event_to_csv(self):
        """Appends time punch event to csv file."""
        with open(PATH_TO_CSV, "a") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([self.time_punched_at.isoformat(), self.project])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project", required=False)
    arguments = parser.parse_args()
    punch_to_log = TimePunchEvent(datetime.utcnow(), arguments.project)
    if os.path.isfile(PATH_TO_CSV):  # If the csv file already exists with punches, then append.
        punch_to_log.append_event_to_csv()
    else:  # If the csv file does not exist, then create new file, write header, and append.
        punch_to_log.write_event_to_new_csv()


if __name__ == "__main__":
    main()
