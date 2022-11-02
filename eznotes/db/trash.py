from . import get_conn_and_cur


def trash_note(note_id):
    conn, cur = get_conn_and_cur()

    cur.execute(f"UPDATE notes SET added_to_trash = 1, trash_date = datetime('now', 'localtime') WHERE id LIKE '{note_id}%'")

    conn.commit()


def empty_trash():
    conn, cur = get_conn_and_cur()

    cur.execute("DELETE FROM notes WHERE added_to_trash = 1")

    conn.commit()


def restore_note(note_id):
    conn, cur = get_conn_and_cur()

    cur.execute(
        f"UPDATE notes SET added_to_trash = 0, trash_date = NULL WHERE id LIKE '{note_id}%'"
    )
    conn.commit()


def get_trash_notes(sort_by, order):
    cur = get_conn_and_cur()[1]
    if sort_by == "alphabetical":
        sort_by = "title"
    cur.execute(f"SELECT * FROM notes WHERE added_to_trash = 1 ORDER BY {sort_by} {order}")
    return cur.fetchall()