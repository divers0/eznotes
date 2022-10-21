import sys

from rich.console import Console

console = Console()


def error_print(error_message):
    console.print("[bold red]Error:[/bold red] " + error_message)


def _error_exit(error_message, exit_status=1):
    error_print(error_message)
    sys.exit(exit_status)


def executable_does_not_exist_error(name):
    _error_exit(f"Executable [green]'{name}'[/green] does not exist.")


def note_not_found_error(note_id):
    _error_exit(f"[green]'{note_id}'[/green] is not the id of any note.")


def note_file_not_saved_error():
    _error_exit("You need the save file after you finished writing the note.")


def note_file_is_executable_error():
    _error_exit("A note file cannot be a executable.")


def program_runned_with_root_access_error():
    _error_exit("Don't Run this app with root access.")


def no_notes_in_db_error():
    _error_exit(
        "Currently there are no notes. see [bold italic]eznotes --help[/bold italic]",
        0
    )
