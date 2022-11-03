import os

from .const import DEFAULT_EDITOR_FILE_PATH
from .logs import DefaultEditorLogs
from .prompt import default_editor_prompt
from .utils import executable_exists


def editor_file_exists():
    return True if os.path.isfile(DEFAULT_EDITOR_FILE_PATH) else False


def change_default_editor(new_editor):
    if executable_exists(new_editor):
        with open(DEFAULT_EDITOR_FILE_PATH, "w") as f:
            f.write(new_editor)
    else:
        from .exceptions import ExecutableDoesNotExist
        raise ExecutableDoesNotExist


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

    logs = DefaultEditorLogs()
    logs.next_log()

    change_default_editor(default_editor_prompt(logs.input_prompt))
