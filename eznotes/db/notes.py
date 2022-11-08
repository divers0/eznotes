from . import get_conn_and_cur


def get_all_notes(sort_by, order):
    cur = get_conn_and_cur()[1]
    if sort_by == "alphabetical":
        sort_by = "text"
    cur.execute(
        "SELECT * FROM notes WHERE added_to_trash = 0 ORDER BY "
        f"{sort_by} {order}"
    )
    return cur.fetchall()


def note_exists(note_id):
    cur = get_conn_and_cur()[1]
    cur.execute(f"SELECT * FROM notes WHERE id LIKE '{note_id}%'")
    if not cur.fetchone():
        return False
    return True


def get_full_note(note_id):
    cur = get_conn_and_cur()[1]
    cur.execute(f"SELECT text FROM notes WHERE id LIKE '{note_id}%'")
    return cur.fetchone()[0]


def get_note_date_created(note_id):
    cur = get_conn_and_cur()[1]
    cur.execute(f"SELECT date_created FROM notes WHERE id LIKE '{note_id}%'")
    return cur.fetchone()


def get_note_date_modified(note_id):
    cur = get_conn_and_cur()[1]
    cur.execute(f"SELECT date_modified FROM notes WHERE id LIKE '{note_id}%'")
    return cur.fetchone()


def get_all_note_ids():
    cur = get_conn_and_cur()[1]
    cur.execute("SELECT id FROM notes WHERE added_to_trash = 0")
    return cur.fetchall()


def get_all_trash_ids():
    cur = get_conn_and_cur()[1]
    cur.execute("SELECT id FROM notes WHERE added_to_trash = 1")
    return cur.fetchall()
