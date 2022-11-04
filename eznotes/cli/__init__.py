import click

from ..config.editor import get_default_editor
from ..const import SORTING_OPTIONS
from ..trash import trash_is_on


@click.group(invoke_without_command=True)
@click.option("-e", "--edit", is_flag=True)
@click.option("-v", "--view", is_flag=True)
@click.option("-d", "--delete", is_flag=True)
@click.option("-x", "--export", is_flag=True)
@click.option(
    "-s", "--sort-by", default="modified",
    type=click.Choice(SORTING_OPTIONS)
)
@click.option("--asc/--desc", "order", default=True)
@click.option("--version", is_flag=True)
@click.pass_context
def cli(ctx, edit, view, delete, export, sort_by, order, version):
    if version:
        from ..const import VERSION
        return print(VERSION)

    if trash_is_on():
        from ..db import get_conn_and_cur

        conn, cur = get_conn_and_cur()

        # Deleting notes that have been in the trash for 30 days or more
        cur.execute(
            "DELETE FROM notes WHERE trash_date <= datetime('now','-30 day')"
        )

        conn.commit()

    if not ctx.invoked_subcommand:
        from ..db.notes import get_all_notes
        from ..exceptions import NoNotesInDatabase
        from ..logs import done_log
        from ..logs.error import no_notes_in_db_error
        from ..utils.notes import fix_sort_by_name
        from .func import list_view

        order = "ASC" if order else "DESC"
        sort_by = fix_sort_by_name(sort_by)

        notes = "\n".join(
            f"{x[0][:8]} - {x[1]}"
            for x in get_all_notes(sort_by, order)
        )

        try:
            print_done = list_view(
                notes,
                False,
                edit=edit,
                view=view,
                delete=delete,
                export=export
            )
        except NoNotesInDatabase:
            no_notes_in_db_error()

        if any((edit, delete, export)) or print_done:
            done_log()


@cli.command()
@click.argument(
    "command",
    default="",
    type=click.Choice(["empty", "on", "off", ""])
)
@click.option("-r", "--restore", is_flag=True)
@click.option("-v", "--view", is_flag=True)
@click.option("-d", "--delete", is_flag=True)
@click.option(
    "-s",
    "--sort-by",
    default="modified",
    type=click.Choice(SORTING_OPTIONS)
)
@click.option("--asc/--desc", "order", default=True)
def trash(command, restore, view, delete, sort_by, order):
    from ..db.trash import get_trash_notes
    from ..exceptions import NoNotesInDatabase, TrashIsAlreadyEmpty
    from ..logs import done_log
    from ..logs.error import (no_notes_in_trash_error,
                              trash_is_already_empty_error,
                              trash_is_turned_off_error)
    from ..trash import trash_is_on
    from ..utils.notes import fix_sort_by_name
    from .func import list_view

    if command == "empty":
        from ..trash import empty_trash

        try:
            empty_trash()
        except TrashIsAlreadyEmpty:
            trash_is_already_empty_error()
        return
    elif command in ["on", "off"]:
        from ..trash import turn_trash
        return turn_trash(command)

    if not trash_is_on():
        trash_is_turned_off_error()

    order = "ASC" if order else "DESC"
    sort_by = fix_sort_by_name(sort_by)

    notes = "\n".join(
        f"{x[0][:8]} - {x[1]}"
        for x in get_trash_notes(sort_by, order)
    )

    try:
        print_done = list_view(
            notes,
            True,
            restore=restore,
            view=view,
            delete2=delete
        )
    except NoNotesInDatabase:
        no_notes_in_trash_error()

    if any((restore, view, delete)) or print_done:
        done_log()


@cli.command()
@click.argument("title", default="")
@click.argument("body", default="")
@click.option(
    "-f", "--finished",
    is_flag=True,
    help="It can be used when you have written the whole note from the command"
        " itself and not from the editor."
)
@click.option(
    "-e",
    "--editor",
    default=get_default_editor(),
    show_default=True
)
def add(title, body, finished, editor):
    from ..exceptions import NoteFileNotSaved
    from ..logs import done_log
    from ..notes import new_note

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
    from .func import get_relevant_func, note_id_command

    note_id_command(note_id, get_relevant_func("edit"), editor)


@cli.command()
@click.argument("note_id")
def view(note_id):
    from .func import get_relevant_func, note_id_command

    note_id_command(note_id, get_relevant_func("view"))


@cli.command()
@click.argument("note_id")
def delete(note_id):
    from .func import get_relevant_func, note_id_command

    note_id_command(note_id, get_relevant_func("delete"))


@cli.command(name="del", help="Alias for delete")
@click.argument("note_id")
def del_command(note_id):
    from .func import get_relevant_func, note_id_command

    note_id_command(note_id, get_relevant_func("delete"))


@cli.command(name="all")
@click.argument(
    "category",
    default="notes",
    type=click.Choice(["notes", "trash"])
)
@click.option(
    "-s",
    "--sort-by",
    default="alphabet",
    type=click.Choice(SORTING_OPTIONS)
)
@click.option("--asc/--desc", "order", default=True)
def all_command(category, sort_by, order):
    from ..logs import pager_view
    from ..utils.notes import fix_sort_by_name

    if category == "notes":
        from ..db.notes import get_all_notes as get_all_func
    else:
        from ..db.trash import get_trash_notes as get_all_func

    order = "ASC" if order else "DESC"
    sort_by = fix_sort_by_name(sort_by)

    notes = "\n".join(
        f"[bold blue]{x[0]}[/] - [green]{x[1]}[/]"
        for x in get_all_func(sort_by, order)
    )

    pager_view(notes)


@cli.command(name="import")
@click.argument(
    "filenames",
    type=click.Path(exists=True, dir_okay=False),
    nargs=-1
)
@click.option("-t", "--title")
@click.option("--filename-as-title", is_flag=True)
def import_command(filenames, title, filename_as_title):
    import magic

    from ..import_note import import_from_zip, import_plain_text
    from ..logs import done_log
    from ..logs.error import error_print
    from ..logs.messages import note_file_is_binary_error_message
    from ..utils import is_file_binary


    print_done = True
    for filename in filenames:
        if magic.from_file(filename, mime=True) == "application/zip":
            import_from_zip(filename)

        # check if the file is a executable
        elif is_file_binary(filename):
            error_print(note_file_is_binary_error_message)
            print_done = False

        else:
            import_plain_text(title, filename_as_title, filename)
    if print_done:
        done_log()


@cli.command()
@click.argument("note_id")
@click.argument("path", default=".", type=click.Path(exists=False))
def export(note_id, path):
    import os

    from ..export import export_note
    from ..logs import done_log
    from ..logs.error import file_not_found_error
    from ..utils import is_path_writable

    if note_id == "all":
        from ..export import export_notes_to_zip

        if os.path.isdir(path):
            path = os.path.join(path, "notes")

        export_notes_to_zip(path)

        return done_log()

    if is_path_writable(path) or os.path.isdir(path):
        export_note(note_id, path)
    else:
        file_not_found_error(path)

    done_log()


@cli.command()
@click.argument("new_editor")
def changeeditor(new_editor):
    from ..config.editor import change_default_editor
    from ..exceptions import ExecutableDoesNotExist
    from ..logs.error import executable_does_not_exist_error

    try:
        change_default_editor(new_editor)
    except ExecutableDoesNotExist:
        executable_does_not_exist_error(new_editor)

