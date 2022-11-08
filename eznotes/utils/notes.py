def get_note_title(note):
    return note.split("\n")[0]


def add_title_and_body_together(title, body):
    return f"{title}\n{body}"


def add_new_title_to_text(note, new_title):
    return "\n".join([new_title+"\n"]+note.split("\n"))


def clean_up_temp_file():
    import os

    from ..const import TEMP_FILE_PATH

    if os.path.exists(TEMP_FILE_PATH):
        os.remove(TEMP_FILE_PATH)


def fix_sort_by_name(sort_by):
    if sort_by == "alphabet":
        return "alphabetical"
    elif sort_by in ["created", "modified"]:
        return "date_"+sort_by
