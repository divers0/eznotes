import getpass
import os
import signal
import sys

from ..config import config_file_initiate, config_file_valid
from ..const import CONFIG_FOLDER_PATH, DATABASE_PATH
from ..db.init import db_initiate
from ..logs.error import program_runned_with_root_access_error


def signal_handler(sig, frame):
    sys.exit(sig)


signal.signal(signal.SIGINT, signal_handler)


def check_for_initiation():
    if not os.path.exists(CONFIG_FOLDER_PATH):
        os.mkdir(CONFIG_FOLDER_PATH)
    if not os.path.exists(DATABASE_PATH):
        db_initiate()
    if not config_file_valid():
        config_file_initiate()


def check_for_root():
    user = getpass.getuser()
    if user == "root":
        program_runned_with_root_access_error()


def main():
    check_for_root()
    check_for_initiation()
    # it has to be here
    from ..cli import cli

    cli()
