more_inf = " see eznotes {command} --help for more information."

add_help_message = "Opens the default editor, after exit adds the note modified buffer to the database."+more_inf.format(command="add")

trash_help_message = "When no arguments are given, it opens the trash in the fzf view."+more_inf.format(command="trash")

edit_help_message = "Opens the default editor with a buffer already filled with the selected note's contents. after exit edits the already existing note with the modified buffer to the database."+more_inf.format(command="edit")

view_help_message = "Opens the selected note's contents just for view. if the program detects that it's written in markdown, it shows the text accordingly."

delete_help_message = "Deletes the selected note."

all_help_message = "Shows all of the notes with their IDs."+more_inf.format(command="all")

import_help_message = "Imports the given file(s) to the database. the given files can be zip (with the structure that program recognises), json (with the structure that program recognises), or plain text."+more_inf.format(command="import")

export_help_message = "Exports the selected note or all of the notes to the given path (OPTIONAL)."+more_inf.format(command="export")

changeeditor_help_message = "Changes the default editor the the given."

__all__ = [x for x in list(locals()) if x.endswith("help_message")]
