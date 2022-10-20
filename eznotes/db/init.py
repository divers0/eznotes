import os

from ..const import CONFIG_FOLDER_PATH, DATABASE_PATH
from . import get_conn_and_cur


def db_initiate():
    # added this because sometimes the editor might be not
    # configured properly and in those cases this function
    # also gets called.
    if os.path.exists(DATABASE_PATH):
        return
    if not os.path.exists(CONFIG_FOLDER_PATH):
        os.mkdir(CONFIG_FOLDER_PATH)
    with open(DATABASE_PATH, 'w') as f:
        f.write('')
    conn, cur = get_conn_and_cur()
    cur.execute('''CREATE TABLE IF NOT EXISTS notes(
                    id TEXT NOT NULL PRIMARY KEY,
                    title TEXT,
                    body TEXT,
                    datetime TEXT);
                            ''')
    conn.commit()
