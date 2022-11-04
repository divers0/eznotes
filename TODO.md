# TODO
 - [x] add a way to have a default editor
 - [x] make a wrapper for edit_note
 - [x] Better logs and errors
 - [x] add del
 - [x] update README.md
 - [x] ability to add notes from files
 - [x] ability to export one note
 - [x] ability to export all of the notes
 - [x] improve delete note output
 - [x] if none of the flags were runned (-v -d -e or whatever), after the fzf screen ask the user what do they want to do with the note
 - [x] make a parent class named Logs and set all the logs classes in logs to be its child. then change the logic to be like this:
    for examples we have two logs that they need to be printed; instead of making a function for each one of them,
    make a list at the `__init__`  with all the log strings in it. then make a function named next_log or whatever
    which uses the counter (which is also defined at `__init__`) and console.prints the item at that index of the list
    that we made earlier.
 - [x] generate the self.options_text at ListViewLogs class instead of hard-coding it.
 - [x] replace all of the error logs outside of cli with exception (which should be added) and handle
       the raised exceptions inside cli.
 - [x] check if the file is binary instead of executable
 - [x] add "Done." logs.
 - [x] add exit as an option in the prompt after fzf
 - [x] add a argument for title in the add command and write that to the file that is going to be opened with editor (body could be added too)
 - [x] if user selected view (in the prompt after fzf) don't exit the prompt
 - [x] move the prompt after fzf to a separate function from list view
 - [x] sort the notes in fzf based on latest updated
 - [x] add a list command which **prints** out all the notes.
 - [x] add the option to sort the fzf list
 - [x] when exporting a single note, change the file date to the notes date (fix its metadata)
 - [x] make a wrapper for view
 - [x] make `del` an alias for `delete`
 - [x] when adding a note from a file extract the files date created and date modified and use those valued in the database
 - [x] change the name of addfromfile to import
 - [x] make a general function for del, delete, view, add and edit for following the DRY code
 - [x] add .txt extension at the end of exported notes (and try to handle that the other way around (in the import function))
 - [x] in the deleting prompt mention the fact that the delete is permanent
 - [x] add import from zip files (`eznotes export all` output)
 - [x] add trash
      - [x] add the column in database
      - [x] make a function for restoring notes back to the db
      - [x] add a fzf view for trash
      - [x] add an empty trash command
      - [x] permanently delete notes that have been trashed more than 30 days
      - [x] export trash in `eznotes export all`
 - [ ] better `--help` output
 - [ ] add colors to the fzf (that opens the possibility to themes in the future?)
 - [x] add a note by default to the db
 - [x] add the ability to turn the trash on or off
 - [x] move the VERSION const to the const.py, then add a '--version' flag
 - [ ] add a `search` command
 - [x] refactor import
 - [ ] merge the title and body columns (idk why i decided that they would be two separate things in the first place)
 - [x] clean
      - [x] in logs, make self.logs tuples not lists
      - [x] try to prevent any line to be more than 80 characters (there are some in logs)
      - [x] clean const.py
