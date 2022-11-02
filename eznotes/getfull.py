import os
import sys

from .db.notes import get_full_note
from .logs import markdown_print


def cli_main():
    from rich.console import Console

    if len(sys.argv) < 2:
        sys.exit()

    note_id = sys.argv[1]
    # color_system could also be set on 'truecolor'
    # https://rich.readthedocs.io/en/stable/console.html#color-systems
    console = Console(color_system="standard")
    md = markdown_print(get_full_note(note_id), print_=False)
    # the reason that i don't use os.get_terminal_size here is that
    # this function gets called when fzf is running and when fzf is running the
    # os.get_terminal_size() function raises an
    # OSError: [Errno 25] Inappropriate ioctl for device
    # error.
    try:
        width = int(os.getenv("COLUMNS")) // 2
    except TypeError:
        width = os.get_terminal_size().columns // 2
    console.print(md, width=width)
