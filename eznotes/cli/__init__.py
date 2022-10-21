import click

from ..default_editor import change_default_editor, get_default_editor
from ..exceptions import NoteFileNotSaved
from .func import new_note, edit_note, delete_note, list_view
from ..logs.error import (
    note_not_found_error,
    note_file_not_saved_error,
    note_file_is_executable_error,
)


@click.group(invoke_without_command=True)
@click.option("-e", "--edit", is_flag=True)
@click.option("-v", "--view", is_flag=True)
@click.option('-d', '--delete', is_flag=True)
@click.option('--change-editor', 'new_editor')
@click.pass_context
def cli(ctx, edit, view, delete, new_editor):
    if not ctx.invoked_subcommand:
        if new_editor:
            change_default_editor(new_editor)

        list_view(edit, view, delete)


@cli.command()
@click.option('-e', '--editor', default=get_default_editor())
def add(editor):
    try:
        new_note(editor)
    except NoteFileNotSaved:
        note_file_not_saved_error()


@cli.command()
@click.argument("note_id")
@click.option("--editor", default=get_default_editor())
def edit(note_id, editor):
    from ..db import note_exists

    if note_exists(note_id):
        edit_note(note_id, editor)
    else:
        note_not_found_error(note_id)


@cli.command(name='del')
@click.argument("note_id")
def del_command(note_id):
    from ..db import note_exists

    if note_exists(note_id):
        delete_note(note_id)
    else:
        note_not_found_error(note_id)


@cli.command()
@click.argument("filename", type=click.Path(exists=True, dir_okay=False))
def addfromfile(filename):
    import os
    from ..db import add_note_to_db

    # check if is a executable
    if os.access(filename, os.X_OK):
        note_file_is_executable_error()
    with open(filename) as f:
        add_note_to_db(f.read())
