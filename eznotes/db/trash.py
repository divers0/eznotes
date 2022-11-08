from . import get_conn_and_cur


def trash_note(note_id):
    conn, cur = get_conn_and_cur()

    cur.execute(
        "UPDATE notes SET added_to_trash = 1, "
        f"trash_date = datetime('now', 'localtime') WHERE id LIKE '{note_id}%'"
    )

    conn.commit()
    return True


def empty_trash():
    conn, cur = get_conn_and_cur()

    cur.execute("DELETE FROM notes WHERE added_to_trash = 1")

    conn.commit()


def restore_note(note_id):
    conn, cur = get_conn_and_cur()

    cur.execute(
        "UPDATE notes SET added_to_trash = 0, trash_date = NULL "
        f"WHERE id LIKE '{note_id}%'"
    )
    conn.commit()


def get_trash_notes(sort_by, order):
    cur = get_conn_and_cur()[1]
    if sort_by == "alphabetical":
        sort_by = "text"
    cur.execute(
        "SELECT * FROM notes WHERE added_to_trash = 1 ORDER BY "
        f"{sort_by} {order}"
    )
    return cur.fetchall()


def trash_is_empty():
    cur = get_conn_and_cur()[1]
    cur.execute("SELECT * FROM notes WHERE added_to_trash = 1")
    return not any(1 for _ in cur.fetchall())
