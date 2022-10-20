import hashlib
import sqlite3
from datetime import datetime
from ..const import DATABASE_PATH



def _make_id(note):
    now = str(datetime.now())
    note_hash = hashlib.md5((note+now).encode()).hexdigest()
    return note_hash


def get_conn_and_cur():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn, conn.cursor()


def insert(row, note):
    conn, cur = get_conn_and_cur()
    note_hash = _make_id(note)
    row = (note_hash, *row)
    cur.execute(
        "INSERT INTO notes VALUES(?, ?, ?, strftime('%Y-%m-%d %H:%M:%S'))", row
    )
    conn.commit()


def get_all_notes():
    conn, cur = get_conn_and_cur()
    cur.execute("SELECT * FROM notes;")
    return cur.fetchall()
