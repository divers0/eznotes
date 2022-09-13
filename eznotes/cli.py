import os
import click
from .db import insert
from .exceptions import NoteFileNotSaved


@click.group()
def cli():
    ...


@click.command()
@click.option('-e', '--editor', default='vim')
def addnote(editor):
    tmp_file_name = '.eznotes'
    tmp_file_path = os.path.join('/tmp', tmp_file_name)

    counter = 1
    while os.path.exists(tmp_file_path):
        tmp_file_path = f"{os.path.join('/tmp', tmp_file_name)} ({counter})"
        counter += 1

    os.system(f"{editor} '{tmp_file_path}'")

    if not os.path.exists(tmp_file_path):
        raise NoteFileNotSaved

    with open(tmp_file_path, 'r') as f:
        text = f.read()

    title = text.split('\n')[0].strip()
    body = '\n'.join(text.split('\n')[1:])

    insert((title, body))


@click.command()
def list():
    ...


commands = (addnote,)
for command in commands:
    cli.add_command(command)

