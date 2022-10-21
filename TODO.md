# TODO
 - [x] add a way to have a default editor
 - [x] make a wrapper for edit_note
 - [x] Better logs and errors
 - [x] add del
 - [ ] update README.md
 - [x] ability to add notes from files
 - [ ] ability to export notes (all or one)
 - [x] improve delete note output
 - [x] if none of the flags were runned (-v -d -e or whatever), after the fzf screen ask the user what do they want to do with the note
 - [ ] make a parent class named Logs and set all the logs classes in logs to be its child. then change the logic to be like this:
    for examples we have two logs that they need to be printed; instead of making a function for each one of them,
    make a list at the \_\_init\_\_  with all the log strings in it. then make a function named next_log or whatever
    which uses the counter (which is also defined at \_\_init\_\_) and console.prints the item at that index of the list
    that we made earlier.
 - [ ] generate the self.options_text at ListViewLogs class instead of hard-coding it.
 - [ ] replace all of the error logs outside of cli with exception (which should be added) and handle
       the raised exceptions inside cli.
 - [x] check if the file is binary instead of executable