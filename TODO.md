# TODO
 - [x] add a way to have a default editor
 - [x] make a wrapper for edit_note
 - [x] Better logs and errors
 - [x] add del
 - [ ] update README.md
 - [x] ability to add notes from files
 - [x] ability to export one note
 - [ ] ability to export all of the notes
 - [x] improve delete note output
 - [x] if none of the flags were runned (-v -d -e or whatever), after the fzf screen ask the user what do they want to do with the note
 - [ ] make a parent class named Logs and set all the logs classes in logs to be its child. then change the logic to be like this:
    for examples we have two logs that they need to be printed; instead of making a function for each one of them,
    make a list at the `__init__`  with all the log strings in it. then make a function named next_log or whatever
    which uses the counter (which is also defined at `__init__`) and console.prints the item at that index of the list
    that we made earlier.
 - [ ] move the input_prompt string from a function to a attribute
 - [x] generate the self.options_text at ListViewLogs class instead of hard-coding it.
 - [x] replace all of the error logs outside of cli with exception (which should be added) and handle
       the raised exceptions inside cli.
 - [x] check if the file is binary instead of executable
 - [x] add "Done." logs.
 - [x] add exit as an option in the prompt after fzf
 - [ ] add a argument for title in the add command and write that to the file that is going to be opened with editor (body could be added too)
 - [x] if user selected view (in the prompt after fzf) don't exit the prompt
 - [ ] move the prompt after fzf to a separate function from list view
 - [x] sort the notes in fzf based on latest updated
 - [ ] add a list command which **prints** out all the notes.
 - [ ] add the option to sort the fzf list
