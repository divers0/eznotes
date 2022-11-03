import hashlib
import sqlite3
from datetime import datetime

from ..const import DATABASE_PATH


def make_id(note):
    now = str(datetime.now())
    note_id = hashlib.md5((note + now).encode()).hexdigest()
    return note_id


def insert(row, note, date=None):
    conn, cur = get_conn_and_cur()
    note_id = make_id(note)
    row = [note_id, *row, 0, None]
    if date:
        row.insert(3, date)
        row.insert(3, date)
        cur.execute("INSERT INTO notes VALUES(?, ?, ?, ?, ?, ?, ?)", row)
    else:
        cur.execute("INSERT INTO notes VALUES(?, ?, ?, datetime('now', 'localtime'), datetime('now', 'localtime'), ?, ?)", row)
    conn.commit()


def get_conn_and_cur():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn, conn.cursor()
