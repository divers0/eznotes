from os.path import dirname, expanduser, join

DEBUG = False

CONFIG_FOLDER_PATH = join(expanduser("~"), ".config", "eznotes")

if DEBUG:
    DATABASE_PATH = join(dirname(dirname(__file__)), "notes.db")
else:
    DATABASE_PATH = join(CONFIG_FOLDER_PATH, "notes.db")

DEFAULT_EDITOR_FILE_PATH = join(CONFIG_FOLDER_PATH, "default_editor")

TEMP_FILE_PATH = "/tmp/.eznotes_tmp"

TEMP_DIR_PATH = "/tmp/.eznotes_notes"

TEMP_ZIP_DIR_PATH = join(TEMP_DIR_PATH, "notes")

TEMP_ZIP_TRASH_DIR_PATH = join(TEMP_DIR_PATH, "notes", "trash")

NOTES_VALID_INPUTS = {
    "edit": ("1", "edit", "e"),
    "view": ("2", "view", "v"),
    "delete": ("3", "delete", "d"),
    "export": ("4", "export", "x"),
}

TRASH_VALID_INPUTS = {
    "delete": ("1", "delete", "d"),
    "view": ("2", "view", "v"),
    "restore": ("3", "restore", "r"),
}
