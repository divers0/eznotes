from .db import get_conn_and_cur


def get_all_notes(sort_by, order):
    cur = get_conn_and_cur()[1]
    if sort_by == "alphabetical":
        sort_by = "title"
    cur.execute(f"SELECT * FROM notes ORDER BY {sort_by} {order}")
    return cur.fetchall()


def get_full_note(note_id):
    cur = get_conn_and_cur()[1]

    cur.execute(f"SELECT * FROM notes WHERE id LIKE '{note_id}%'")
    note = cur.fetchone()
    return f"{note[1]}\n{note[2]}"


def note_exists(note_id):
    cur = get_conn_and_cur()[1]
    cur.execute(f"SELECT * FROM notes WHERE id LIKE '{note_id}%'")
    if not cur.fetchone():
        return False
    return True


def add_note_to_db(text, date=None):
    from .db import insert

    title, body = get_title_and_body(text)

    insert((title, body), text, date)


def get_note_title(note_id):
    cur = get_conn_and_cur()[1]
    cur.execute(f"SELECT title FROM notes WHERE id LIKE '{note_id}%'")
    return cur.fetchone()


def get_note_body(note_id):
    cur = get_conn_and_cur()[1]
    cur.execute(f"SELECT body FROM notes WHERE id LIKE '{note_id}%'")
    return cur.fetchone()


def get_title_and_body(note_text):
    return note_text.split("\n")[0].strip(), "\n".join(note_text.split("\n")[1:])


def get_note_date_created(note_id):
    cur = get_conn_and_cur()[1]
    cur.execute(f"SELECT date_created FROM notes WHERE id LIKE '{note_id}%'")
    return cur.fetchone()


def get_note_date_modified(note_id):
    cur = get_conn_and_cur()[1]
    cur.execute(f"SELECT date_modified FROM notes WHERE id LIKE '{note_id}%'")
    return cur.fetchone()


def get_all_ids():
    cur = get_conn_and_cur()[1]
    cur.execute("SELECT id FROM notes")
    return cur.fetchall()


def export_notes_to_zip(path):
    import json
    import os
    import shutil

    from .cli.func import export_note
    from .const import TEMP_DIR_PATH, TEMP_ZIP_DIR_PATH

    try:
        shutil.rmtree(TEMP_DIR_PATH)
    except FileNotFoundError:
        ...

    os.makedirs(TEMP_ZIP_DIR_PATH)

    all_note_ids = get_all_ids()

    for note_id in all_note_ids:
        export_note(note_id[0], TEMP_ZIP_DIR_PATH)

    notes_dict = {"notes": []}

    rows = get_all_notes("title", "ASC")

    for _, title, body, date_modified, date_created in rows:
        notes_dict["notes"].append({
            "title": title,
            "body": body,
            "date_modified": date_modified,
            "date_created": date_created,

        })

    with open(os.path.join(TEMP_ZIP_DIR_PATH, "notes.json"), "w") as f:
        f.write(json.dumps(notes_dict, indent=4))

    shutil.make_archive(os.path.splitext(path)[0] if path.endswith(".zip") else path, "zip", TEMP_DIR_PATH)

    shutil.rmtree(TEMP_DIR_PATH)
