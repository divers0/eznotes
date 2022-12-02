# eznotes
read and write notes inside of your terminal


# Install
**DISCLAIMER: This program has been designed to work on linux. no support is provided to any user on any other OS.**
## Requirements
 - python
 - [fzf](https://github.com/junegunn/fzf)


1. install fzf
2. after installing fzf you can simply download the the latest release from the [releases page](https://github.com/divers0/eznotes/releases/latest)
3. after downloading the release, run the following commands (replace VERSION with the last version)
```console
$ tar xf eznotes-VERSION.tar.gz
$ cd eznotes-VERSION
$ pip install .
```

# Usage

## Your Default editor
if it's the first time that you are running the program, you'll see a prompt that will ask you what is
your preferred editor.

## Adding your first note
after that, you can simply run
```
eznotes add
```
for your default editor that you selected at the previous time to be opened\

## List of your notes
```
eznotes
```

## Editing, Viewing, Deleting and Exporting
for all the actions above there are two ways to approach
##### 1. the first way is to just run `eznotes` and select your note there, then just pick what you want to do with the note in the next prompt that will pop up automatically

##### 2. the second way is to just memorize what is the hash (id) of the note that you want, then just run
```
eznotes COMMAND NOTE_ID
```

### List of commands that you can use with the explanation above
 - `edit`
 - `view`
 - `delete` or `del`
 - `export`

## Trash
by default, whenever you delete a note it does not get permanently deleted. instead it goes to a place called the trash\
now that i have amazed you with that fact, let's see how you can use trash:
### Viewing your trash
```
eznotes trash
```
### Restoring, viewing or deleteing a note from trash
again just like above there are two ways of approaching this actions
1. use a flag. like `-r` (`--restore`) or `-v` (`--view`) or `-d` (`--delete`) or
2. just run `eznotes trash` and after you selected a note, just use the prompt

### Emptying your trash
```
eznotes trash empty
```

### Turning trash on/off
```
eznotes trash [on/off]
```

## Exporting all of your notes
the explanation for exporting only one note was mentioned above.\
but when you have more than 5 notes, it gets hard to export them all.
well there is an easy way to export all of your notes:
```
eznotes export all [PATH]
```
you can easily export all of your commands to a zip file.

## Add a note from a file (import)
```
eznotes import FILENAME
```
the selected file can be plain text
or a zip file.\
zip files either have to be the output of `eznotes export all` or if they are not
they have to follow the structure that the program uses when exporting all the notes.

see `eznotes import --help` for more information

## Changing your default editor
in the future if you decided that you want to change your default editor, don't worry i've got you covered.
it's as simple as it gets:
```
eznotes changeeditor NEW_EDITOR
```
## More information

see `eznotes --help` for more information
