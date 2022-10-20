import os
from .db import insert
from .exceptions import NoteFileNotSaved
from .getfull import get_full


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
