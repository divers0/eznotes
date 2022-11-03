import os

from ..const import CONFIG_FOLDER_PATH, DATABASE_PATH, FIRST_NOTE_TEXT
from ..utils.notes import get_title_and_body
from . import get_conn_and_cur, insert


def db_initiate():
    # added this because sometimes the editor might be not
    # configured properly and in those cases this function
    # also gets called.
    if os.path.exists(DATABASE_PATH):
        return

    if not os.path.exists(CONFIG_FOLDER_PATH):
        os.mkdir(CONFIG_FOLDER_PATH)

    with open(DATABASE_PATH, "w") as f:
        f.write("")

    conn, cur = get_conn_and_cur()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS notes(
                    id TEXT NOT NULL PRIMARY KEY,
                    title TEXT,
                    body TEXT,
                    date_modified TEXT,
                    date_created TEXT,
                    added_to_trash INTEGER,
                    trash_date TEXT);"""
    )

    insert(get_title_and_body(FIRST_NOTE_TEXT))
    conn.commit()
