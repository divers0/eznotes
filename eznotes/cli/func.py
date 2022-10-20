import os

from ..db import get_all_notes, insert
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
    note_hash = note.split()[0]
    full_note = get_full(note_hash)

    tmp_file_path = _get_new_file()

    with open(tmp_file_path, 'w') as f:
        f.write(full_note)

    os.system(f"{editor} '{tmp_file_path}'")


def list_view(view):
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

    if view:
        from rich.console import Console
        from rich.markdown import Markdown

        from ..getfull import get_full

        console = Console()
        md = Markdown(get_full(selected_note.split()[0]))
        with console.pager():
            console.print(md)
    else:
        editor = get_default_editor()
        edit_note(selected_note, editor)
