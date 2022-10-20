import click

from ..default_editor import change_default_editor, get_default_editor
from ..exceptions import NoteFileNotSaved
from ..utils import executable_exists
from .func import add_note, delete_note, list_view


@click.group(invoke_without_command=True)
@click.option("-v", "--view", is_flag=True)
@click.option('-d', '--delete', is_flag=True)
@click.option('--change-editor', 'new_editor')
@click.pass_context
def cli(ctx, view, delete, new_editor):
    if not ctx.invoked_subcommand:
        if new_editor:
            if executable_exists(new_editor):
                change_default_editor(new_editor)
            else:
                print(f"Executable '{new_editor}' does not exist.")
        selected_note = list_view(delete, view)
        if delete:
            if not selected_note:
                # TODO
                print("In order to delete a note, you have to select one first.")
                return
            note_id = selected_note.split()[0]
            delete_note(note_id)


@cli.command()
@click.option('-e', '--editor', default=get_default_editor())
def add(editor):
    try:
        add_note(editor)
    except NoteFileNotSaved:
        # TODO
        print("You need the save the note file.")


@cli.command(name='del')
@click.argument("note_id")
def del_command(note_id):
    from ..db import note_exists
    if note_exists(note_id):
        delete_note(note_id)
    else:
        # TODO
        print(f"'{note_id}' does not belong to any note.")
