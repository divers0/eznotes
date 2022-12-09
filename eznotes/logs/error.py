import sys

from rich.console import Console

from .messages import *

console = Console()


def error_print(error_message):
    console.print("[bold red]Error:[/bold red] " + error_message)


def _error_exit(error_message, exit_status=1):
    error_print(error_message)
    sys.exit(exit_status)


def executable_does_not_exist_error(name):
    _error_exit(executable_does_not_exist_error_message.format(name=name))


def note_not_found_error(note_id):
    _error_exit(note_not_found_error_message.format(note_id=note_id))


def note_file_not_saved_error():
    _error_exit(note_file_not_saved_error_message)


def program_runned_with_root_access_error():
    _error_exit(program_runned_with_root_access_error_message)


def no_notes_in_db_error():
    _error_exit(
        no_notes_in_db_error_message,
        0
    )


def no_notes_in_trash_error():
    _error_exit(
        no_notes_in_trash_error_message,
        0
    )


def file_not_found_error(path):
    _error_exit(file_not_found_error_message.format(path=path))


def finished_without_text_error():
    _error_exit(finished_without_text_error_message)


def unrecognized_file_error(filename):
    _error_exit(unrecognized_file_error_message.format(filename=filename))


def trash_is_turned_off_error():
    _error_exit(trash_is_turned_off_error_message, 0)


def trash_is_already_empty_error():
    _error_exit(trash_is_already_empty_error_message, 0)


def not_on_linux_error():
    _error_exit(not_on_linux_error_message)
