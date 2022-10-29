import os


def note_id_command(note_id, func, *args):
    from ..logs import done_log
    from ..notes import note_exists

    if note_exists(note_id):
        func(note_id, *args)
    else:
        from ..logs.error import note_not_found_error

        note_not_found_error(note_id)
    done_log()


def clean_up_temp_file():
    from ..const import TEMP_FILE_PATH

    if os.path.exists(TEMP_FILE_PATH):
        os.remove(TEMP_FILE_PATH)


def new_note(title, body, finished, editor):
    from ..const import TEMP_FILE_PATH
    from ..exceptions import NoteFileNotSaved
    from ..notes import add_note_to_db

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
    from ..const import TEMP_FILE_PATH
    from ..db import get_conn_and_cur
    from ..notes import get_full_note, get_title_and_body

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
        f"UPDATE notes SET title = ?, body = ?, date_modified = strftime('%Y-%m-%d %H:%M:%S') WHERE id LIKE '{note_id}%'",
        (title, body),
    )
    conn.commit()


def view_note(note_id):
    from ..logs import markdown_print, pager_view
    from ..notes import get_full_note

    pager_view(markdown_print(get_full_note(note_id), print_=False))


def delete_note(note_id):
    from rich.prompt import Confirm

    from ..db import get_conn_and_cur
    from ..logs import DeleteNoteLogs, markdown_print, panel_print
    from ..notes import get_full_note

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


# TODO: move this function elsewhere
def _export_note_prompt(note_id):
    from ..logs import ExportNoteLogs, NoPromptSuffixPrompt
    from ..logs.error import error_print
    from ..logs.messages import file_not_found_error_message
    from ..notes import get_note_title
    from ..utils import is_path_writable

    logs = ExportNoteLogs()
    logs.next_log()

    while True:
        entered_path = NoPromptSuffixPrompt.ask(logs.input_prompt, default=".")

        if os.path.isdir(entered_path):
            return os.path.join(entered_path, get_note_title(note_id)[0])
        elif is_path_writable(entered_path):
            return entered_path
        else:
            error_print(file_not_found_error_message.format(path=entered_path))


def export_note(note_id, path):
    import os
    from datetime import datetime

    from ..notes import (
        get_full_note,
        get_title_and_body,
        get_note_date_created,
        get_note_date_modified,
    )

    full_note = get_full_note(note_id)

    title = get_title_and_body(full_note)[0]

    if os.path.isdir(path):
        path = os.path.join(path, title)

    if not path.endswith(".txt"):
        path += ".txt"

    with open(path, "w") as f:
        f.write(full_note)

    date_created, time_created = get_note_date_created(note_id)[0].split(" ")
    date_modified, time_modified = get_note_date_modified(note_id)[0].split(" ")

    created_timestamp = datetime(*map(int, date_created.split('-')), *map(int, time_created.split(':'))).timestamp()
    modified_timestamp = datetime(*map(int, date_modified.split('-')), *map(int, time_modified.split(':'))).timestamp()

    os.utime(path, (created_timestamp, modified_timestamp))


def list_view(edit, view, delete, export, sort_by, order):
    from ..default_editor import get_default_editor
    from ..notes import get_all_notes

    notes = "\n".join(f"{x[0][:8]} - {x[1]}" for x in get_all_notes(sort_by, order))
    if notes == "":
        from ..exceptions import NoNotesInDatabase
        raise NoNotesInDatabase

    selected_note = (
        os.popen(
            f'echo "{notes}" | '
            'fzf --reverse --preview "eznotes-getfull {1}" '
            f"--preview-window right,{os.get_terminal_size().columns//2}"
        )
        .read()
        .strip()
    )

    if selected_note == "":
        return

    note_id = selected_note.split()[0]

    if edit:
        editor = get_default_editor()
        edit_note(note_id, editor)

    elif view:
        view_note(note_id)

    elif delete:
        delete_note(note_id)

    elif export:
        from ..logs.error import file_not_found_error

        path = _export_note_prompt(note_id)

        try:
            export_note(note_id, path)
        except FileNotFoundError:
            file_not_found_error(path)

    else:
        from ..const import VALID_INPUTS
        from ..logs import (ListViewLogs, NoPromptSuffixPrompt,
                            selected_note_log)
        from ..utils import flatten

        selected_note_log(note_id)

        logs = ListViewLogs(VALID_INPUTS.values())

        logs.next_log(note_id=note_id)
        logs.next_log()

        choices = flatten(VALID_INPUTS.values())+["exit"]
        while True:
            user_inp = NoPromptSuffixPrompt.ask(f"[bold white]\[{'/'.join(choices)}]", choices=choices, default="edit", show_choices=False)

            if user_inp in VALID_INPUTS["edit"]:
                editor = get_default_editor()
                edit_note(note_id, editor)
                return True

            elif user_inp in VALID_INPUTS["view"]:
                view_note(note_id)

            elif user_inp in VALID_INPUTS["delete"]:
                return delete_note(note_id)

            elif user_inp in VALID_INPUTS["export"]:
                from ..logs.error import file_not_found_error

                path = _export_note_prompt(note_id)

                try:
                    export_note(note_id, path)
                except FileNotFoundError:
                    file_not_found_error(path)

                export_note(note_id, path)
                return True

            elif user_inp == "exit":
                return
