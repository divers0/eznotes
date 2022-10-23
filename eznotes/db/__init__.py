import hashlib
import sqlite3
from datetime import datetime

from ..const import DATABASE_PATH


def _make_id(note):
    now = str(datetime.now())
    note_id = hashlib.md5((note + now).encode()).hexdigest()
    return note_id


def insert(row, note):
    conn, cur = get_conn_and_cur()
    note_id = _make_id(note)
    row = (note_id, *row)
    cur.execute("INSERT INTO notes VALUES(?, ?, ?, strftime('%Y-%m-%d %H:%M:%S'), strftime('%Y-%m-%d %H:%M:%S'))", row)
    conn.commit()


def get_conn_and_cur():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn, conn.cursor()
