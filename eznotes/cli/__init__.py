import click
from ..utils import executable_exists
from .func import add_note, list_view
from ..default_editor import get_default_editor, change_default_editor


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
    add_note(editor)
