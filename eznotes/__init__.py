import getpass
import os
import signal
import sys

from rich.console import Console

from .const import DATABASE_PATH
from .db.init import db_initiate
from .default_editor import editor_file_exists, editor_initiate


def signal_handler(sig, frame):
    print('\nExiting....')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


console = Console()


def check_for_initiation():
    if os.path.exists(DATABASE_PATH) and editor_file_exists():
        return True
    return False


def check_for_root():
    user = getpass.getuser()
    if user == 'root':
        console.print("Don't Run this app with root access.", style='bold red')
        sys.exit(1)


def main():
    check_for_root()
    if not check_for_initiation():
        db_initiate()
        editor_initiate()
    # it has to be here
    from .cli import cli
    cli()
