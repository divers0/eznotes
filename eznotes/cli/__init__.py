import click

from ..default_editor import change_default_editor, get_default_editor
from ..exceptions import NoteFileNotSaved
from ..utils import executable_exists
from .func import add_note, list_view


@click.group(invoke_without_command=True)
@click.option("-v", "--view", is_flag=True)
@click.option('--change-editor', 'new_editor')
@click.pass_context
def cli(ctx, view, new_editor):
    if not ctx.invoked_subcommand:
        if new_editor:
            if executable_exists(new_editor):
                change_default_editor(new_editor)
            else:
                print(f"Executable '{new_editor}' does not exist.")
        list_view(view)


@cli.command()
@click.option('-e', '--editor', default=get_default_editor())
def addnote(editor):
    try:
        add_note(editor)
    except NoteFileNotSaved:
        # TODO
        print("You need the save the note file.")
