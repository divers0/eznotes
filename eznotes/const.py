from os.path import expanduser, join

CONFIG_FOLDER_PATH = join(expanduser("~"), ".config", "eznotes")

DATABASE_PATH = join(CONFIG_FOLDER_PATH, "notes.db")

DEFAULT_EDITOR_FILE_PATH = join(CONFIG_FOLDER_PATH, "default_editor")

TEMP_FILE_PATH = "/tmp/.eznotes_tmp"

TEMP_DIR_PATH = "/tmp/.eznotes_notes"

TEMP_ZIP_DIR_PATH = join(TEMP_DIR_PATH, "notes")

VALID_INPUTS = {
    "edit": ("1", "edit", "e"),
    "view": ("2", "view", "v"),
    "delete": ("3", "delete", "d"),
    "export": ("4", "export", "x"),
}
