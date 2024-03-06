import sqlite3


def read_sql_from_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()


def connect_to_db(db_file_path: str) -> sqlite3.Connection:
    return sqlite3.connect(db_file_path)


def generate_daily_report(conn: sqlite3.Connection, sql_path: str) -> None:
    # TODO: Docstring comment
    with conn:
        result = conn.execute(read_sql_from_file(sql_path)).fetchall()
    width = 40
    print("Hour Totals by Category")
    for row in result:
        print(row[0].ljust(width) + str(row[1]).ljust(width))


def retrieve_open_punches(conn: sqlite3.Connection, sql_path: str) -> None:
    # TODO: Docstring comment
    with conn:
        result = conn.execute(read_sql_from_file(sql_path)).fetchall()
    width = 20
    print("Open Punches")
    for row in result:
        print(row[1].ljust(width) + str(row[0]).ljust(width))
