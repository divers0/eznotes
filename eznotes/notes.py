def new_note(title, body, finished, editor):
    import os

    from .const import TEMP_FILE_PATH
    from .db.notes import add_note_to_db
    from .exceptions import NoteFileNotSaved
    from .utils.notes import clean_up_temp_file

    clean_up_temp_file()
    if title:
        preset_text = title+"\n"
        if body != "":
            preset_text += body
        if finished:
            add_note_to_db(preset_text)
            return
        with open(TEMP_FILE_PATH, "w") as f:
            f.write(preset_text)

    os.system(f"{editor} '{TEMP_FILE_PATH}'")

    if not os.path.exists(TEMP_FILE_PATH):
        raise NoteFileNotSaved

    with open(TEMP_FILE_PATH, "r") as f:
        text = f.read()

    add_note_to_db(text)


def edit_note(note_id, editor):
    import os

    from .const import TEMP_FILE_PATH
    from .db import get_conn_and_cur
    from .db.notes import get_full_note, get_title_and_body
    from .utils.notes import clean_up_temp_file

    full_note = get_full_note(note_id)

    with open(TEMP_FILE_PATH, "w") as f:
        f.write(full_note)

    os.system(f"{editor} '{TEMP_FILE_PATH}'")

    with open(TEMP_FILE_PATH, "r") as f:
        edited_note = f.read()

    clean_up_temp_file()

    title, body = get_title_and_body(edited_note)

    conn, cur = get_conn_and_cur()

    cur.execute(
        f"UPDATE notes SET title = ?, body = ?, date_modified = datetime('now', 'localtime') WHERE id LIKE '{note_id}%'",
        (title, body),
    )
    conn.commit()


def view_note(note_id):
    from .db.notes import get_full_note
    from .logs import markdown_print, pager_view

    pager_view(markdown_print(get_full_note(note_id), print_=False))


def delete_note(note_id):
    from rich.prompt import Confirm

    from .db import get_conn_and_cur
    from .db.notes import get_full_note
    from .logs import DeleteNoteLogs, markdown_print, panel_print

    conn, cur = get_conn_and_cur()

    logs = DeleteNoteLogs(note_id)

    panel_print(
        markdown_print(
            "\n".join(get_full_note(note_id).split("\n")[:4]),
            print_=False
        ),
        title=logs.title
    )

    if Confirm.ask(logs.input_prompt):
        cur.execute(f"DELETE FROM notes WHERE id LIKE '{note_id}%'")
        conn.commit()
        return True
    return False
