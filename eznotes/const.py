import os

CONFIG_FOLDER_PATH = os.path.join(os.path.expanduser("~"), ".config", "eznotes")

DATABASE_PATH = os.path.join(CONFIG_FOLDER_PATH, "notes.db")

DEFAULT_EDITOR_FILE_PATH = os.path.join(CONFIG_FOLDER_PATH, 'default_editor')
