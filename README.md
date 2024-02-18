## Cli Chronicler

A command line app for keeping track of project/work times.

### Features

* Keep track of when you punch in and out for the day.
* Keep track of project times by using an optional description flag.
* View a report of hours for the current day.

### Installation

```Bash
pip install cli-chronicler
```

### Usage

#### Punch In/Out Without Description

```Bash
punch
```

#### Punch In/Out With Description

```Bash
punch -d 'pypi project development'
```

#### View Today's Report

```Bash
punch -r
```

#### View Open Punches

```Bash
punch -o
```