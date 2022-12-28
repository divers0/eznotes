import sys

from rich.console import Console

from ..db.notes import get_full_note
from ..logs import markdown_print


def cli_main():
    if len(sys.argv) < 2:
        sys.exit()

    note_id = sys.argv[1]
    width = int(sys.argv[2])
    # color_system could also be set on 'truecolor'
    # https://rich.readthedocs.io/en/stable/console.html#color-systems
    console = Console(color_system="standard")

    md = markdown_print(get_full_note(note_id), print_=False)

    console.print(md, width=width)
