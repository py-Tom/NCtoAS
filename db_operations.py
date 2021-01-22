"""Module for performing operations on the database."""


import sqlite3

conn = sqlite3.connect("settings.db")
c = conn.cursor()


def insert(table, name, coord):
    with conn:
        c.execute(
            f"INSERT INTO {table} VALUES (:name, :coord)",
            {"name": name, "coord": coord},
        )
    return None


def select(table, name, coord):
    c.execute(f"SELECT {coord} FROM {table} WHERE name=:name", {"name": name})
    return c.fetchone()[0]


def update(table, name, coord):
    c.execute(
        f"UPDATE {table} SET coord=:coord WHERE name=:name",
        {"name": name, "coord": coord},
    )
    return None


def remove(table, name):
    with conn:
        c.execute(f"DELETE from {table} WHERE name=:name", {"name": name})
    return None


def select_table(table):
    c.execute(f"SELECT * FROM {table}")
    return c.fetchall()[0]


def select_name(table):
    c.execute(f"SELECT name FROM {table}")
    return c.fetchall()


def update_previous(
    nc_path,
    as_path,
    base,
    tool,
    rapid_speed,
    rapid_accuracy,
    line_speed,
    line_accuracy,
    circular_speed,
    circular_accuracy,
    options_speed,
    options_base,
):
    with conn:
        c.execute(
            """UPDATE previous SET
                                nc_path=:nc_path,
                                as_path=:as_path,
                                base=:base,
                                tool=:tool,
                                rapid_speed=:rapid_speed,
                                rapid_accuracy=:rapid_accuracy,
                                line_speed=:line_speed,
                                line_accuracy=:line_accuracy,
                                circular_speed=:circular_speed,
                                circular_accuracy=:circular_accuracy,
                                options_speed=:options_speed,
                                options_base=:options_base""",
            {
                "nc_path": nc_path,
                "as_path": as_path,
                "base": base,
                "tool": tool,
                "rapid_speed": rapid_speed,
                "rapid_accuracy": rapid_accuracy,
                "line_speed": line_speed,
                "line_accuracy": line_accuracy,
                "circular_speed": circular_speed,
                "circular_accuracy": circular_accuracy,
                "options_speed": options_speed,
                "options_base": options_base,
            },
        )
    return None


def insert_previous(
    nc_path,
    as_path,
    base,
    tool,
    rapid_speed,
    rapid_accuracy,
    line_speed,
    line_accuracy,
    circular_speed,
    circular_accuracy,
    options_speed,
    options_base,
):
    with conn:
        c.execute(
            """INSERT INTO previous VALUES (:nc_path, :as_path, :base, :tool, :rapid_speed, :rapid_accuracy, 
                    :line_speed, :line_accuracy, :circular_speed, :circular_accuracy, :options_speed, :options_base)""",
            {
                "nc_path": nc_path,
                "as_path": as_path,
                "base": base,
                "tool": tool,
                "rapid_speed": rapid_speed,
                "rapid_accuracy": rapid_accuracy,
                "line_speed": line_speed,
                "line_accuracy": line_accuracy,
                "circular_speed": circular_speed,
                "circular_accuracy": circular_accuracy,
                "options_speed": options_speed,
                "options_base": options_base,
            },
        )
    return None


if __name__ == "__main__":
    # Create database tables
    c.execute(
        """CREATE TABLE previous (
                nc_path text,
                as_path text,
                base text,
                tool text,
                rapid_speed integer,
                rapid_accuracy integer,
                line_speed integer,
                line_accuracy integer,
                circular_speed integer,
                circular_accuracy integer,
                options_speed bool,
                options_base bool
            )"""
    )

    conn.commit()

    c.execute(
        """CREATE TABLE base (
                name text,
                coord text
            )"""
    )

    conn.commit()

    c.execute(
        """CREATE TABLE tool (
                name text,
                coord text
            )"""
    )

    conn.commit()
    conn.close()
