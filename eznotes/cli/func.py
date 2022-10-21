import os


def clean_up_temp_file():
    from ..const import TEMP_FILE_PATH

    if os.path.exists(TEMP_FILE_PATH):
        os.remove(TEMP_FILE_PATH)


def new_note(editor):
    from ..const import TEMP_FILE_PATH
    from ..db import add_note_to_db
    from ..exceptions import NoteFileNotSaved

    clean_up_temp_file()
    os.system(f"{editor} '{TEMP_FILE_PATH}'")

    if not os.path.exists(TEMP_FILE_PATH):
        raise NoteFileNotSaved

    with open(TEMP_FILE_PATH, "r") as f:
        text = f.read()

    add_note_to_db(text)


def edit_note(note_id, editor):
    from ..const import TEMP_FILE_PATH
    from ..db import get_conn_and_cur
    from ..getfull import get_full
    from ..utils import get_title_and_body

    full_note = get_full(note_id)

    with open(TEMP_FILE_PATH, "w") as f:
        f.write(full_note)

    os.system(f"{editor} '{TEMP_FILE_PATH}'")

    with open(TEMP_FILE_PATH, "r") as f:
        edited_note = f.read()

    clean_up_temp_file()

    title, body = get_title_and_body(edited_note)

    conn, cur = get_conn_and_cur()

    cur.execute(
        f"UPDATE notes SET title = ?, body = ? WHERE id LIKE '{note_id}%'",
        (title, body),
    )
    conn.commit()


def delete_note(note_id):
    from rich.prompt import Confirm

    from ..db import get_conn_and_cur
    from ..getfull import get_full
    from ..logs import DeleteNoteLogs, markdown_print, panel_print

    conn, cur = get_conn_and_cur()

    logs = DeleteNoteLogs(note_id)

    panel_print(
        markdown_print(
            "\n".join(get_full(note_id).split("\n")[:4]),
            print_=False
        ),
        title=logs.title()
    )

    if Confirm.ask(logs.input_prompt()):
        cur.execute(f"DELETE FROM notes WHERE id LIKE '{note_id}%'")
        conn.commit()


def list_view(edit, view, delete):
    from ..db import get_all_notes
    from ..default_editor import get_default_editor
    from ..getfull import get_full
    from ..logs import markdown_print, pager_view
    from ..logs.error import no_notes_in_db_error

    notes = "\n".join([f"{x[0][:8]} - {x[1]}" for x in get_all_notes()])
    if notes == "":
        no_notes_in_db_error()

    selected_note = (
        os.popen(
            f'echo "{notes}" | '
            f'fzf --reverse --preview "eznotes-getfull {{1}}" '
            f"--preview-window right,{os.get_terminal_size().columns//2}"
        )
        .read()
        .strip()
    )

    if selected_note == "":
        return

    note_id = selected_note.split()[0]

    if not any((edit, view, delete)):
        from ..const import VALID_INPUTS
        from ..logs import ListViewLogs, NoPromptSuffixPrompt

        logs = ListViewLogs()

        logs.first(note_id)
        logs.second()

        # user_inp = NoPromptSuffixPrompt.ask(logs.input_prompt(note_id), choices=VALID_INPUTS, default="edit", show_choices=False)
        user_inp = NoPromptSuffixPrompt.ask(choices=VALID_INPUTS, default="edit")

        if user_inp in ("1", "edit", "e"):
            editor = get_default_editor()
            edit_note(note_id, editor)

        elif user_inp in ("2", "view", "v"):
            pager_view(markdown_print(get_full(note_id), print_=False))

        elif user_inp in ("3", "delete", "d"):
            delete_note(note_id)
        return

    if edit:
        editor = get_default_editor()
        edit_note(note_id, editor)

    elif view:
        pager_view(markdown_print(get_full(note_id), print_=False))

    elif delete:
        delete_note(note_id)
