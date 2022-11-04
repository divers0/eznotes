import json
import os
import shutil
from datetime import datetime

from .const import TEMP_DIR_PATH, TEMP_ZIP_DIR_PATH, TEMP_ZIP_TRASH_DIR_PATH
from .db.notes import (get_all_note_ids, get_all_notes, get_all_trash_ids,
                       get_full_note, get_note_date_created,
                       get_note_date_modified)
from .db.trash import get_trash_notes
from .utils.notes import get_title_and_body


def export_note(note_id, path):
    full_note = get_full_note(note_id)

    title = get_title_and_body(full_note)[0]

    if os.path.isdir(path):
        path = os.path.join(path, title)

    if not path.endswith(".txt"):
        path += ".txt"

    with open(path, "w") as f:
        f.write(full_note)

    date_created, time_created = get_note_date_created(note_id)[0].split(" ")
    date_modified, time_modified = get_note_date_modified(note_id)[0].split(" ")

    created_timestamp = datetime(
        *map(int, date_created.split("-")),
        *map(int, time_created.split(":"))).timestamp()
    modified_timestamp = datetime(
        *map(int, date_modified.split("-")),
        *map(int, time_modified.split(":"))).timestamp()

    os.utime(path, (created_timestamp, modified_timestamp))


def export_notes_to_zip(path):
    try:
        shutil.rmtree(TEMP_DIR_PATH)
    except FileNotFoundError:
        ...

    os.makedirs(TEMP_ZIP_TRASH_DIR_PATH)

    note_ids = get_all_note_ids()
    trash_ids = get_all_trash_ids()

    for note_id in note_ids:
        export_note(note_id[0], TEMP_ZIP_DIR_PATH)

    for note_id in trash_ids:
        export_note(note_id[0], os.path.join(TEMP_ZIP_DIR_PATH, "trash"))

    notes_dict = {"notes": [], "trash": []}

    rows = get_all_notes("title", "ASC")
    trash_rows = get_trash_notes("title", "ASC")

    # Adding the notes
    for _, title, body, date_modified, date_created, _, _ in rows:
        notes_dict["notes"].append({
            "title": title,
            "body": body,
            "date_modified": date_modified,
            "date_created": date_created,

        })

    # Adding the notes in trash
    for _, title, body, date_modified, date_created, _, trash_date \
            in trash_rows:
        notes_dict["trash"].append({
            "title": title,
            "body": body,
            "date_modified": date_modified,
            "date_created": date_created,
            "trash_date": trash_date,
        })

    with open(os.path.join(TEMP_ZIP_DIR_PATH, "notes.json"), "w") as f:
        f.write(json.dumps(notes_dict, indent=4))

    shutil.make_archive(
        os.path.splitext(path)[0] if path.endswith(".zip") else path,
        "zip", TEMP_DIR_PATH
    )

    shutil.rmtree(TEMP_DIR_PATH)
