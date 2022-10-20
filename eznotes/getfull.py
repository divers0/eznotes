import os
import sys
from .db import get_conn_and_cur


def cli_main():
    from rich.console import Console
    from rich.markdown import Markdown

    if len(sys.argv) < 2:
        sys.exit()

    note_hash = sys.argv[1]
    console = Console()
    md = Markdown(get_full(note_hash))
    # the reason that i don't use os.get_terminal_size here is that
    # this function gets called when fzf is running and when fzf is running the
    # os.get_terminal_size() function raises an
    # OSError: [Errno 25] Inappropriate ioctl for device
    # error.
    width = int(os.getenv("COLUMNS"))//2
    console.print(md, width=width)


def get_full(note_hash):
    conn, cur = get_conn_and_cur()

    cur.execute(f"SELECT * FROM notes WHERE id like '{note_hash}%'")
    note = cur.fetchone()
    return f"{note[1]}\n{note[2]}"
