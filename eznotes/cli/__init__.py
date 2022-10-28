import click

from ..default_editor import get_default_editor
from ..exceptions import NoNotesInDatabase, NoteFileNotSaved


@click.group(invoke_without_command=True)
@click.option("-e", "--edit", is_flag=True)
@click.option("-v", "--view", is_flag=True)
@click.option("-d", "--delete", is_flag=True)
@click.option("-x", "--export", is_flag=True)
@click.option("-s", "--sort-by", default="date_modified", type=click.Choice(["alphabetical", "date_created", "date_modified"]))
@click.option("--asc/--desc", "order", default=True)
@click.pass_context
def cli(ctx, edit, view, delete, export, sort_by, order):
    if not ctx.invoked_subcommand:
        from .func import list_view
        from ..logs import done_log
        from ..logs.error import no_notes_in_db_error

        try:
            # If it was on ascending
            if order:
                order = "ASC"
            # If it was on descending
            else:
                order = "DESC"
            print_done = list_view(edit, view, delete, export, sort_by, order)
            if any((edit, delete, export)) or print_done:
                done_log()
        except NoNotesInDatabase:
            no_notes_in_db_error()


@cli.command()
@click.argument("title", default="")
@click.argument("body", default="")
@click.option(
    "-f", "--finished",
    is_flag=True,
    help="It can be used when you have written the whole note from the command"
        " itself and not from the editor."
)
@click.option("-e", "--editor", default=get_default_editor(), show_default=True)
def add(title, body, finished, editor):
    from ..logs import done_log
    from .func import new_note

    if title == "":
        title = None

    if not title and finished:
        from ..logs.error import finished_without_text_error

        finished_without_text_error()


    try:
        new_note(title, body, finished, editor)
    except NoteFileNotSaved:
        from ..logs.error import note_file_not_saved_error

        note_file_not_saved_error()

    done_log()


@cli.command()
@click.argument("note_id")
@click.option("--editor", default=get_default_editor(), show_default=True)
def edit(note_id, editor):
    from .func import edit_note, note_id_command

    note_id_command(note_id, edit_note, editor)


@cli.command()
@click.argument("note_id")
def view(note_id):
    from .func import view_note, note_id_command

    note_id_command(note_id, view_note)


@cli.command()
@click.argument("note_id")
def delete(note_id):
    from .func import delete_note, note_id_command

    note_id_command(note_id, delete_note)


@cli.command(name="del", help="Alias for delete")
@click.argument("note_id")
def del_command(note_id):
    from .func import delete_note, note_id_command

    note_id_command(note_id, delete_note)


@cli.command(name="all")
def all_command():
    from ..notes import get_all_notes
    from ..logs import pager_view

    notes = "\n".join(f"[bold blue]{x[0]}[/] - [green]{x[1]}[/]" for x in get_all_notes())

    pager_view(notes)


@cli.command(name="import")
@click.argument("filename", type=click.Path(exists=True, dir_okay=False))
@click.option("-t", "--title")
@click.option("--filename-as-title", is_flag=True)
def import_command(filename, title, filename_as_title):
    from ..logs import done_log
    from ..logs.error import note_file_is_binary_error
    from ..notes import add_note_to_db
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


@cli.command()
@click.argument("note_id")
@click.argument("path", default=".", type=click.Path(exists=False))
def export(note_id, path):
    import os

    from ..logs import done_log
    from ..logs.error import file_not_found_error
    from ..utils import is_path_writable
    from .func import export_note

    if is_path_writable(path) or os.path.isdir(path):
        export_note(note_id, path)
    else:
        file_not_found_error(path)

    done_log()


@cli.command()
@click.argument("new_editor")
def changeeditor(new_editor):
    from ..default_editor import change_default_editor
    from ..exceptions import ExecutableDoesNotExist
    from ..logs.error import executable_does_not_exist_error

    try:
        change_default_editor(new_editor)
    except ExecutableDoesNotExist:
        executable_does_not_exist_error(new_editor)
