import os

from ..db import get_all_notes, insert, get_conn_and_cur
from ..default_editor import get_default_editor
from ..exceptions import NoteFileNotSaved
from ..getfull import get_full
from ..utils import get_title_and_body
from ..const import TEMP_FILE_PATH


def clean_up_temp_file():
    if os.path.exists(TEMP_FILE_PATH):
        os.remove(TEMP_FILE_PATH)


def add_note(editor):
    clean_up_temp_file()
    os.system(f"{editor} '{TEMP_FILE_PATH}'")

    if not os.path.exists(TEMP_FILE_PATH):
        raise NoteFileNotSaved

    with open(TEMP_FILE_PATH, 'r') as f:
        text = f.read()

    title, body = get_title_and_body(text)

    insert((title, body), text)


def edit_note(note, editor):
    note_id = note.split()[0]
    full_note = get_full(note_id)

    with open(TEMP_FILE_PATH, 'w') as f:
        f.write(full_note)

    os.system(f"{editor} '{TEMP_FILE_PATH}'")

    with open(TEMP_FILE_PATH, 'r') as f:
        new_note = f.read()

    clean_up_temp_file()

    title, body = get_title_and_body(new_note)

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


def list_view(delete, view):
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

    if delete:
        return selected_note

    if view:
        from rich.console import Console
        from rich.markdown import Markdown

        from ..getfull import get_full

        console = Console()
        md = Markdown(get_full(selected_note.split()[0]))
        with console.pager(styles=True):
            console.print(md)
    else:
        editor = get_default_editor()
        edit_note(selected_note, editor)
