import re


def executable_exists(name):
    from shutil import which

    return which(name) is not None


# this function can be improved so much over time
# it could have improved a lot right now if i knew more regex but unfortunately
# my regex knowledge ends here.
def text_is_markdown(text):
    if any(1 for _ in re.findall("\*\*[a-zA-Z0-9].*\*\*", text)):
        return True
    if any(1 for _ in re.findall("_[a-zA-Z0-9].*_", text)):
        return True
    for i in text.split("\n"):
        if i.startswith(("# ", "- ", " - ", "1. ")):
            return True
    return False


def is_file_binary(file_path):
    with open(file_path, "rb") as f:
        file_bytes = f.read(1024)

    textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})

    return bool(file_bytes.translate(None, textchars))


def flatten(l):
    return [item for sublist in l for item in sublist]


def is_path_writable(path):
    try:
        open(path, "w").close()
    except (FileNotFoundError, IsADirectoryError, PermissionError):
        return False
    return True


def find_default_editor_executable():
    editors = ("nano", "vim")
    for editor in editors:
        if executable_exists(editor):
            return editor
    return None
