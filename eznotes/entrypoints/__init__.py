import getpass
import os
import platform
import signal
import sys

from ..config import config_file_initiate, config_file_valid
from ..const import CONFIG_DIR_PATH, DATABASE_PATH
from ..db.init import db_initiate
from ..logs.error import (not_on_linux_error,
                          program_runned_with_root_access_error)


def signal_handler(sig, frame):
    sys.exit(sig)


signal.signal(signal.SIGINT, signal_handler)


def check_for_initiation():
    if not os.path.exists(CONFIG_DIR_PATH):
        os.mkdir(CONFIG_DIR_PATH)
    if not os.path.exists(DATABASE_PATH):
        db_initiate()
    if not config_file_valid():
        config_file_initiate()


def check_for_root():
    user = getpass.getuser()
    if user == "root":
        program_runned_with_root_access_error()


def check_for_os():
    if platform.system() != "Linux":
        not_on_linux_error()


def main():
    check_for_os()
    check_for_root()
    check_for_initiation()
    # it has to be here
    from ..cli import cli

    cli()
