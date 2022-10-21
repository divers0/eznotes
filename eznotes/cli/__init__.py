import click

from ..default_editor import get_default_editor
from ..exceptions import NoteFileNotSaved, NoNotesInDatabase


@click.group(invoke_without_command=True)
@click.option("-e", "--edit", is_flag=True)
@click.option("-v", "--view", is_flag=True)
@click.option("-d", "--delete", is_flag=True)
@click.option("--change-editor", "new_editor")
@click.pass_context
def cli(ctx, edit, view, delete, new_editor):
    from ..default_editor import change_default_editor
    from ..exceptions import ExecutableDoesNotExist
    from ..logs.error import executable_does_not_exist_error, no_notes_in_db_error

    if not ctx.invoked_subcommand:
        if new_editor:
            try:
                change_default_editor(new_editor)
            except ExecutableDoesNotExist:
                executable_does_not_exist_error(new_editor)

        from .func import list_view

        try:
            list_view(edit, view, delete)
        except NoNotesInDatabase:
            no_notes_in_db_error()


@cli.command()
@click.option("-e", "--editor", default=get_default_editor())
def add(editor):
    from .func import new_note
    from ..logs import done_log

    try:
        new_note(editor)
    except NoteFileNotSaved:
        from ..logs.error import note_file_not_saved_error

        note_file_not_saved_error()

    done_log()


@cli.command()
@click.argument("note_id")
@click.option("--editor", default=get_default_editor())
def edit(note_id, editor):
    from ..db import note_exists
    from .func import edit_note
    from ..logs import done_log

    if note_exists(note_id):
        edit_note(note_id, editor)
    else:
        from ..logs.error import note_not_found_error

        note_not_found_error(note_id)
    done_log()


@cli.command(name="del")
@click.argument("note_id")
def del_command(note_id):
    from ..db import note_exists
    from .func import delete_note
    from ..logs import done_log

    if note_exists(note_id):
        delete_note(note_id)
    else:
        from ..logs.error import note_not_found_error

        note_not_found_error(note_id)
    done_log()


@cli.command()
@click.argument("filename", type=click.Path(exists=True, dir_okay=False))
@click.option("-t", "--title")
@click.option("--filename-as-title", is_flag=True)
def addfromfile(filename, title, filename_as_title):
    from ..db import add_note_to_db
    from ..logs import done_log
    from ..logs.error import note_file_is_binary_error
    from ..utils import add_new_title_to_text, is_file_binary

    # check if the file is a executable
    if is_file_binary(filename):
        note_file_is_binary_error()

    with open(filename) as f:
        note_file = f.read()

    if title or filename_as_title:
        note_file = add_new_title_to_text(
            note_file,
            title if title else filename.replace("_", " ").replace("-", " ")
        )

    add_note_to_db(note_file)
    done_log()
