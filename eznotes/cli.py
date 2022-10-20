import os
import click
from .db import get_all_notes
from .utils import executable_exists
from .notes import add_note, edit_note
from .default_editor import get_default_editor, change_default_editor


@click.group()
@click.option('--change-editor', 'new_editor')
def cli(new_editor):
    if new_editor:
        if executable_exists(new_editor):
            change_default_editor(new_editor)
        else:
            print(f"Executable '{new_editor}' does not exist.")


@cli.command()
@click.option('-e', '--editor', default=get_default_editor())
def addnote(editor):
    add_note(editor)


@cli.command()
@click.argument("view", type=click.Choice(["edit", "view"]), default="edit")
def list(view):
    notes = '\n'.join([f"{x[0][:8]} - {x[1]}" for x in get_all_notes()])
    if notes == '':
        print("Currently there are no notes. see eznotes --help")
        return
    selected_note = os.popen(
        f"echo \"{notes}\" | "
        f"fzf --reverse --preview \"eznotes-getfull {{1}}\" "
        f"--preview-window right,{os.get_terminal_size().columns//2}"
    ).read().strip()
    if selected_note == '':
        return

    if view == 'edit':
        editor = get_default_editor()
        edit_note(selected_note, editor)
    else:
        from rich.console import Console
        from rich.markdown import Markdown
        from .getfull import get_full

        console = Console()
        md = Markdown(get_full(selected_note.split()[0]))
        with console.pager():
            console.print(md)
