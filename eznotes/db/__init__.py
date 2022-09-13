import os
import sqlite3


CONFIG_FOLDER_PATH = os.path.join(os.path.expanduser("~"), ".config", "eznotes")
DATABASE_PATH = os.path.join(CONFIG_FOLDER_PATH, "notes.db")


def get_conn_and_cur():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn, conn.cursor()

def insert(row):
    conn, cur = get_conn_and_cur()
    cur.execute("INSERT INTO notes VALUES(?, ?, strftime('%Y-%m-%d %H:%M:%S'))", row)
    conn.commit()

