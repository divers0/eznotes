import os
import sys
import signal
import getpass
from .cli import cli
from .db import DATABASE_PATH
from .db.init import initiate
from rich.console import Console


def signal_handler(sig, frame):
    print('\nExiting....')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


console = Console()


def check_for_initiation():
    if os.path.exists(DATABASE_PATH):
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
        initiate()
    cli()
