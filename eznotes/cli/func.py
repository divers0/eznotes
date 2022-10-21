import os

from ..db import get_all_notes, add_note_to_db, get_conn_and_cur
from ..default_editor import get_default_editor
from ..exceptions import NoteFileNotSaved
from ..getfull import get_full
from ..utils import get_title_and_body
from ..const import TEMP_FILE_PATH


def clean_up_temp_file():
    if os.path.exists(TEMP_FILE_PATH):
        os.remove(TEMP_FILE_PATH)


def new_note(editor):
    clean_up_temp_file()
    os.system(f"{editor} '{TEMP_FILE_PATH}'")

    if not os.path.exists(TEMP_FILE_PATH):
        raise NoteFileNotSaved

    with open(TEMP_FILE_PATH, 'r') as f:
        text = f.read()

    add_note_to_db(text)


def edit_note(note_id, editor):
    full_note = get_full(note_id)

    with open(TEMP_FILE_PATH, 'w') as f:
        f.write(full_note)

    os.system(f"{editor} '{TEMP_FILE_PATH}'")

    with open(TEMP_FILE_PATH, 'r') as f:
        edited_note = f.read()

    clean_up_temp_file()

    title, body = get_title_and_body(edited_note)

    conn, cur = get_conn_and_cur()

    cur.execute(f"UPDATE notes SET title = ?, body = ? WHERE id LIKE '{note_id}%'", (title, body))
    conn.commit()


def delete_note(note_id):
    from ..utils import markdown_print

    conn, cur = get_conn_and_cur()
    print(f"'{note_id}' first 3 lines:")
    markdown_print('\n'.join(get_full(note_id).split('\n')[:4]))

    user_inp = ''
    while user_inp not in ['y', 'n']:
        user_inp = input(f"Are you sure you want to delete the '{note_id}' note? [y/n] ")

    if user_inp == 'y':
        cur.execute(f"DELETE FROM notes WHERE id LIKE '{note_id}%'")
        conn.commit()
    else:
        return


def list_view(edit, view, delete):
    notes = '\n'.join([f"{x[0][:8]} - {x[1]}" for x in get_all_notes()])
    if notes == '':
        print("Currently there are no notes. see eznotes --help")
        return
    selected_note = os.popen(
        f"echo \"{notes}\" | "
        f"fzf --reverse --preview \"eznotes-getfull {{1}}\" "
        f"--preview-window right,{os.get_terminal_size().columns//2}"
    ).read().strip()
    if selected_note == '':
        return

    note_id = selected_note.split()[0]
    if delete:
        return selected_note

    if view:
        from ..getfull import get_full
        from ..utils import markdown_print, pager_view

        pager_view(markdown_print(get_full(note_id), print_=False))
    elif edit:
        editor = get_default_editor()
        edit_note(note_id, editor)

    if not edit and not view and not delete:
        valid_inputs = ('1', '2', '3', 'edit', 'view', 'delete', 'e', 'v', 'd')
        print(f"What do you want to do with the note '{note_id}'?")
        print("""1. [1/edit/e]
2. [2/view/v]
3. [3/delete/d]""")

        while True:
            user_inp = input(f"[{note_id}] > ").lower()
            if user_inp in valid_inputs:
                break
            if user_inp != '':
                print(f"'{user_inp}' is not a valid option.")
        print()

        if user_inp in ('1', 'edit', 'e'):
            editor = get_default_editor()
            edit_note(note_id, editor)

        elif user_inp in ('2', 'view', 'v'):
            from ..getfull import get_full
            from ..utils import markdown_print, pager_view

            pager_view(markdown_print(get_full(note_id), print_=False))

        elif user_inp in ('3', 'delete', 'v'):
            delete_note(note_id)

