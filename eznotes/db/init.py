import os

from ..const import DATABASE_PATH, FIRST_NOTE_TEXT
from . import get_conn_and_cur, insert


def db_initiate():
    # added this because sometimes the editor might be not
    # configured properly and in those cases this function
    # also gets called.
    if os.path.exists(DATABASE_PATH):
        return

    with open(DATABASE_PATH, "w") as f:
        f.write("")

    conn, cur = get_conn_and_cur()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS notes(
                    id TEXT NOT NULL PRIMARY KEY,
                    text TEXT,
                    date_modified TEXT,
                    date_created TEXT,
                    added_to_trash INTEGER,
                    trash_date TEXT);"""
    )

    insert(FIRST_NOTE_TEXT)
    conn.commit()
