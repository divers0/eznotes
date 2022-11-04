from ..logs import DefaultEditorLogs
from ..prompt import default_editor_prompt
from ..utils import executable_exists
from . import (change_value_in_conf, config_file_has_key,
               get_value_from_config_file)


def change_default_editor(new_editor):
    if not executable_exists(new_editor):
        from ..exceptions import ExecutableDoesNotExist
        raise ExecutableDoesNotExist

    change_value_in_conf("editor", new_editor)


def get_default_editor():
    return get_value_from_config_file("editor")


def editor_initiate():
    # added this because sometimes the db might be not
    # configured properly and in those cases this function
    # also gets called.
    if config_file_has_key("editor"):
        return

    logs = DefaultEditorLogs()
    logs.next_log()

    change_default_editor(default_editor_prompt(logs.input_prompt))
