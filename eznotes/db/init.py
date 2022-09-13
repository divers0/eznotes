import os
from . import get_conn_and_cur, CONFIG_FOLDER_PATH, DATABASE_PATH


def initiate():
    if not os.path.exists(CONFIG_FOLDER_PATH):
        os.mkdir(CONFIG_FOLDER_PATH)
    with open(DATABASE_PATH, 'w') as f:
        f.write('')
    conn, cur = get_conn_and_cur()
    cur.execute('''CREATE TABLE IF NOT EXISTS notes(
                    title TEXT,
                    body TEXT,
                    datetime TEXT);
                            ''')
    conn.commit()
