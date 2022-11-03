def get_title_and_body(note_text):
    return note_text.split("\n")[0].strip(), "\n".join(note_text.split("\n")[1:])


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
