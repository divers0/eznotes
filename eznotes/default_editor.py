import os
import readline
from .utils import executable_exists
from .const import DEFAULT_EDITOR_FILE_PATH


def editor_file_exists():
    return True if os.path.isfile(DEFAULT_EDITOR_FILE_PATH) else False


def change_default_editor(new_editor):
    with open(DEFAULT_EDITOR_FILE_PATH, 'w') as f:
        f.write(new_editor)


def get_default_editor():
    with open(DEFAULT_EDITOR_FILE_PATH) as f:
        default_editor = f.read().strip()
    return default_editor


def editor_initiate():
    # added this because sometimes the db might be not
    # configured properly and in those cases this function
    # also gets called.
    if editor_file_exists():
        return
    editor_exists = False
    while not editor_exists:
        print(
            "Please enter the name of your default editor (it can be changed later)"
        )
        new_editor = input("Editor (leave blank for 'vim'): ")
        if new_editor == '':
            new_editor = 'vim'
        editor_exists = executable_exists(new_editor)
    change_default_editor(new_editor)
