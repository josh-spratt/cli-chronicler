## 0.6.2

Released on February 20, 2024.

### Fixed

* A bug that would cause the app to crash when running `punch -o` when there was an open punch with a `NULL` description field.

## 0.6.1

Released on February 19, 2024.

### Fixed

* A bug that prevented users who pip installed from initializing the sqlite database file.

## 0.6.0

Released on February 18, 2024.

### Added

* A new feature that provides a list of open punches.

## 0.5.1

Released on February 18, 2024.

### Fixed

* A typo in the README.

## 0.5.0

Released on February 18, 2024.

### Added

* A new feature that provides a report of the current day.

## 0.4.0

Released on February 17, 2024.

### Changed

* Added logic to use the `README.md` contents as the PyPi description.

## 0.3.0

Released on February 17, 2024.

### Changed

* Restructured the project to conform to necessary structure to distribute via PyPi.

## 0.2.0

Released on February 4, 2024.

### Changed

* SQLite database files rather than csv files for storing data.
* UTC and local timestamps for when the event occurred, rather than just UTC.
* Optional flag changed from "project" to "description" to make it more general.

## 0.1.0

Released on February 3, 2024.

### Added

* A minimum viable product.
* Command line app functionality includes:
    * The ability to track the timestamp of an event without context of "what" the event is.
    * The optional ability to add a descriptive field (project) to the event.
    * Write the events to an output csv file.
