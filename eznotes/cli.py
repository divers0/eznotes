import os
import click
from .db import insert


@click.group()
def cli():
    ...

@click.command()
@click.option('-e', '--editor', default='vim')
def addnote(editor):
    tmp_file_path = os.path.join('/tmp', '.eznotes')
    counter = 1
    while os.path.exists(tmp_file_path):
        tmp_file_path = f"{tmp_file_path} ({counter})"
        counter += 1

    os.system(f"{editor} '{tmp_file_path}'")
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

