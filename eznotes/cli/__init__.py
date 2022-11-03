import click

from ..const import FZF_SORTING_OPTIONS
from ..db import get_conn_and_cur
from ..default_editor import get_default_editor


@click.group(invoke_without_command=True)
@click.option("-e", "--edit", is_flag=True)
@click.option("-v", "--view", is_flag=True)
@click.option("-d", "--delete", is_flag=True)
@click.option("-x", "--export", is_flag=True)
@click.option("-s", "--sort-by", default="modified", type=click.Choice(FZF_SORTING_OPTIONS))
@click.option("--asc/--desc", "order", default=True)
@click.option("--version", is_flag=True)
@click.pass_context
def cli(ctx, edit, view, delete, export, sort_by, order, version):
    if version:
        from ..const import VERSION
        return print(VERSION)

    conn, cur = get_conn_and_cur()

    # Deleting notes that have been in the trash for 30 days or more
    cur.execute("DELETE FROM notes WHERE trash_date <= datetime('now','-30 day')")

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

        notes = "\n".join(f"{x[0][:8]} - {x[1]}" for x in get_all_notes(sort_by, order))

        try:
            print_done = list_view(notes, False, edit=edit, view=view, delete=delete, export=export)
        except NoNotesInDatabase:
            no_notes_in_db_error()

        if any((edit, delete, export)) or print_done:
            done_log()


@cli.command()
@click.option("-r", "--restore", is_flag=True)
@click.option("-v", "--view", is_flag=True)
@click.option("-d", "--delete", is_flag=True)
@click.option("-s", "--sort-by", default="modified", type=click.Choice(FZF_SORTING_OPTIONS))
@click.option("--asc/--desc", "order", default=True)
def trash(restore, view, delete, sort_by, order):
    from ..db.trash import get_trash_notes
    from ..exceptions import NoNotesInDatabase
    from ..logs import done_log
    from ..logs.error import no_notes_in_trash_error
    from ..utils.notes import fix_sort_by_name
    from .func import list_view

    order = "ASC" if order else "DESC"
    sort_by = fix_sort_by_name(sort_by)

    notes = "\n".join(f"{x[0][:8]} - {x[1]}" for x in get_trash_notes(sort_by, order))

    try:
        print_done = list_view(notes, True, restore=restore, view=view, delete2=delete)
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
@click.option("-e", "--editor", default=get_default_editor(), show_default=True)
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


# TODO: maybe add sorting
@cli.command(name="all")
def all_command():
    from ..db.notes import get_all_notes
    from ..logs import pager_view

    notes = "\n".join(f"[bold blue]{x[0]}[/] - [green]{x[1]}[/]" for x in get_all_notes("alphabetical", "ASC"))

    pager_view(notes)


@cli.command(name="import")
@click.argument("filename", type=click.Path(exists=True, dir_okay=False))
@click.option("-t", "--title")
@click.option("--filename-as-title", is_flag=True)
def import_command(filename, title, filename_as_title):
    import os
    from datetime import datetime

    import magic

    from ..db.notes import add_note_to_db
    from ..logs import done_log
    from ..logs.error import note_file_is_binary_error
    from ..utils import is_file_binary
    from ..utils.notes import add_new_title_to_text

    if magic.from_file(filename, mime=True) == "application/zip":
        import json
        from zipfile import ZipFile

        from ..db import get_conn_and_cur, make_id
        from ..logs.error import unrecognized_zip_file_error

        conn, cur = get_conn_and_cur()

        with ZipFile(filename) as f:
            try:
                database = json.loads(f.open("notes/notes.json").read())
            except KeyError:
                unrecognized_zip_file_error(filename)

            for note in database["notes"]:
                row = (make_id(f"{note['title']}\n{note['body']}"), note['title'], note['body'], note['date_modified'], note['date_created'])
                cur.execute("INSERT INTO notes VALUES(?, ?, ?, ?, ?, 0, NULL)", row)

            for note in database["trash"]:
                row = (make_id(f"{note['title']}\n{note['body']}"), note['title'], note['body'], note['date_modified'], note['date_created'], note['trash_date'])
                cur.execute("INSERT INTO notes VALUES(?, ?, ?, ?, ?, 1, ?)", row)

        conn.commit()

        return done_log()

    # check if the file is a executable
    elif is_file_binary(filename):
        note_file_is_binary_error()

    with open(filename) as f:
        note_file = f.read()

    last_modified_date = datetime.fromtimestamp(os.stat(filename)[-2]).strftime("%Y-%m-%d %H:%M:%S")

    if title or filename_as_title:
        if filename_as_title and filename.endswith(".txt"):
            filename = os.path.splitext(filename)[0]
        note_file = add_new_title_to_text(
            note_file,
            title if title else filename.replace("_", " ").replace("-", " ")
        )

    add_note_to_db(note_file, last_modified_date)
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
    from ..default_editor import change_default_editor
    from ..exceptions import ExecutableDoesNotExist
    from ..logs.error import executable_does_not_exist_error

    try:
        change_default_editor(new_editor)
    except ExecutableDoesNotExist:
        executable_does_not_exist_error(new_editor)


@cli.command()
def emptytrash():
    from rich.console import Console
    from rich.prompt import Confirm

    from ..db.trash import empty_trash, get_trash_notes
    from ..logs import EmptyTrashNotes, done_log


    logs = EmptyTrashNotes()
    logs.next_log()

    console = Console()

    notes = "\n".join(f"\t[bold blue]{x[0]}[/] - [green]{x[1]}[/]" for x in get_trash_notes("alphabetical", "ASC"))

    console.print(notes)

    if Confirm.ask(logs.input_prompt):
        empty_trash()
        done_log()
