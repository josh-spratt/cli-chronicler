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
