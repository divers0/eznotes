import os
import sqlite3
from . import CONFIG_FOLDER_PATH, DATABASE_PATH


def initiate():
    if not os.path.exists(CONFIG_FOLDER_PATH):
        os.mkdir(CONFIG_FOLDER_PATH)
    with open(DATABASE_PATH, 'w') as f:
        f.write('')
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS notes(
                    title TEXT,
                    body TEXT,
                    datetime TEXT);
                            ''')
