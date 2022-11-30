import os


def note_id_command(note_id, func, *args):
    from ..db.notes import note_exists
    from ..logs import done_log

    if note_exists(note_id):
        func(note_id, *args)
    else:
        from ..logs.error import note_not_found_error

        note_not_found_error(note_id)
    done_log()


def get_relevant_func(name):
    from ..db.trash import restore_note, trash_note
    from ..export import export_note
    from ..notes import delete_note, edit_note, view_note
    from ..trash import trash_is_on

    func_names = {
        "edit": edit_note,
        "view": view_note,
        "delete": trash_note if trash_is_on() else delete_note,
        "export": export_note,
        "restore": restore_note,
        "delete2": delete_note,
    }
    return func_names[name]


def run_relevant_func(note_id=None, **args):
    from ..export import export_note
    from ..notes import edit_note
    from ..prompt import export_note_prompt

    func = [
        (name, get_relevant_func(name))
        for name, true in zip(args.keys(), args.values()) if true
    ][0]
    if func[0] == "edit":
        from ..config.editor import get_default_editor

        editor = get_default_editor()
        edit_note(note_id, editor)
        return
    elif func[0] == "export":
        from ..logs.error import file_not_found_error

        path = export_note_prompt(note_id)

        try:
            export_note(note_id, path)
        except FileNotFoundError:
            file_not_found_error(path)
        return

    return func[1](note_id)


def list_view(notes, is_trash, **commands):
    from ..prompt import notes_prompt, trash_prompt

    if notes == "":
        from ..exceptions import NoNotesInDatabase
        raise NoNotesInDatabase

    selected_note = (
        os.popen(
            f'echo "{notes}" | '
            'fzf --with-nth 3.. --reverse --preview "eznotes-getfull {1}" '
            f"--preview-window right,{os.get_terminal_size().columns//2}"
        )
        .read()
        .strip()
    )

    if selected_note == "":
        return

    note_id = selected_note.split()[0]

    if any(commands.values()):
        return run_relevant_func(note_id, **commands)

    if is_trash:
        return trash_prompt(note_id)
    else:
        return notes_prompt(note_id)
