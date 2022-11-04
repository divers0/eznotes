from os.path import dirname, expanduser, join


VERSION = "0.7.5"

DEBUG = True

FIRST_NOTE_TEXT = """# welcome the eznotes
## hi there!

you can try some of the features on this note (keep delete for the last one)

# What is this?

this is a simple app for taking notes inside of your command line with your favorite editors!

the goal of this program is to be a simple note taking app that whenever you have anything
(text based obviously) you can easily store.
"""

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

SORTING_OPTIONS = ["alphabet", "created", "modified"]
