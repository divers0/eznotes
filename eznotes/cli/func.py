import os

from ..db import get_all_notes, insert, get_conn_and_cur
from ..default_editor import get_default_editor
from ..exceptions import NoteFileNotSaved
from ..getfull import get_full


def _get_new_file():
    tmp_file_name = '.eznotes'
    tmp_file_path = os.path.join('/tmp', tmp_file_name)

    counter = 1
    while os.path.exists(tmp_file_path):
        tmp_file_path = f"{os.path.join('/tmp', tmp_file_name)} ({counter})"
        counter += 1

    return tmp_file_path


def add_note(editor):
    tmp_file_path = _get_new_file()
    os.system(f"{editor} '{tmp_file_path}'")

    if not os.path.exists(tmp_file_path):
        raise NoteFileNotSaved

    with open(tmp_file_path, 'r') as f:
        text = f.read()

    title = text.split('\n')[0].strip()
    body = '\n'.join(text.split('\n')[1:])

    insert((title, body), text)


def edit_note(note, editor):
    note_id = note.split()[0]
    full_note = get_full(note_id)

    tmp_file_path = _get_new_file()

    with open(tmp_file_path, 'w') as f:
        f.write(full_note)

    os.system(f"{editor} '{tmp_file_path}'")
    # TODO: actually commit the changes into the db :)


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
