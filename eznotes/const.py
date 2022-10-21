import os

CONFIG_FOLDER_PATH = os.path.join(os.path.expanduser("~"), ".config", "eznotes")

DATABASE_PATH = os.path.join(CONFIG_FOLDER_PATH, "notes.db")

DEFAULT_EDITOR_FILE_PATH = os.path.join(CONFIG_FOLDER_PATH, "default_editor")

TEMP_FILE_PATH = "/tmp/.eznotes_tmp"

VALID_INPUTS = ("1", "2", "3", "edit", "view", "delete", "e", "v", "d")
