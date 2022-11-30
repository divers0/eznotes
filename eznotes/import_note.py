import json
import os
from datetime import datetime
from zipfile import ZipFile

from .db import get_conn_and_cur, insert, make_id
from .logs.error import unrecognized_file_error
from .utils.notes import add_new_title_to_text


def import_from_dict(database):
    conn, cur = get_conn_and_cur()

    for note in database["notes"]:
        row = (
            make_id(note["text"]),
            note["text"],
            note["date_modified"],
            note["date_created"]
        )
        cur.execute(
            "INSERT INTO notes VALUES(?, ?, ?, ?, 0, NULL)",
            row
        )

    for note in database["trash"]:
        row = (
            make_id(note["text"]),
            note["text"],
            note["date_modified"],
            note["date_created"],
            note["trash_date"]
        )
        cur.execute("INSERT INTO notes VALUES(?, ?, ?, ?, 1, ?)", row)

    conn.commit()


def import_from_zip(filename):

    with ZipFile(filename) as f:
        try:
            database = json.loads(f.open("notes/notes.json").read())
        except KeyError:
            unrecognized_file_error(filename)

    import_from_dict(database)


def import_plain_text(title, filename_as_title, filename):
    with open(filename) as f:
        note_file = f.read()

    last_modified_date = datetime.fromtimestamp(
        os.stat(filename)[-2]).strftime("%Y-%m-%d %H:%M:%S")

    if title or filename_as_title:
        if filename_as_title and filename.endswith(".txt"):
            filename = os.path.splitext(filename)[0]
        note_file = add_new_title_to_text(
            note_file,
            title if title else filename.replace("_", " ").replace("-", " ")
        )

    insert(note_file, last_modified_date)
