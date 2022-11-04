from rich.prompt import Prompt


class NoPromptSuffixPrompt(Prompt):
    prompt_suffix = " "


def notes_prompt(note_id):
    from .config.editor import get_default_editor
    from .const import NOTES_VALID_INPUTS
    from .db.trash import trash_note
    from .export import export_note
    from .logs import ListViewLogs, selected_note_log
    from .notes import edit_note, view_note
    from .utils import flatten

    selected_note_log(note_id)

    logs = ListViewLogs(NOTES_VALID_INPUTS.values())

    logs.next_log(note_id=note_id)
    logs.next_log()

    choices = flatten(NOTES_VALID_INPUTS.values())+["exit"]
    while True:
        user_inp = NoPromptSuffixPrompt.ask(f"[bold white]\[{'/'.join(choices)}]", choices=choices, default="edit", show_choices=False)

        if user_inp == "exit":
            return

        elif user_inp in NOTES_VALID_INPUTS["edit"]:
            editor = get_default_editor()
            edit_note(note_id, editor)
            return True

        elif user_inp in NOTES_VALID_INPUTS["view"]:
            view_note(note_id)

        elif user_inp in NOTES_VALID_INPUTS["delete"]:
            trash_note(note_id)
            return True

        elif user_inp in NOTES_VALID_INPUTS["export"]:
            from .logs.error import file_not_found_error

            path = export_note_prompt(note_id)

            try:
                export_note(note_id, path)
            except FileNotFoundError:
                file_not_found_error(path)

            export_note(note_id, path)
            return True


def trash_prompt(note_id):
    from .const import TRASH_VALID_INPUTS
    from .db.trash import restore_note
    from .logs import ListViewLogs, selected_note_log
    from .notes import delete_note, view_note
    from .utils import flatten

    selected_note_log(note_id)

    logs = ListViewLogs(TRASH_VALID_INPUTS.values())

    logs.next_log(note_id=note_id)
    logs.next_log()

    choices = flatten(TRASH_VALID_INPUTS.values())+["exit"]
    while True:
        user_inp = NoPromptSuffixPrompt.ask(f"[bold white]\[{'/'.join(choices)}]", choices=choices, default="delete", show_choices=False)

        if user_inp == "exit":
            return

        elif user_inp in TRASH_VALID_INPUTS["delete"]:
            delete_note(note_id)
            return True

        elif user_inp in TRASH_VALID_INPUTS["view"]:
            view_note(note_id)

        elif user_inp in TRASH_VALID_INPUTS["restore"]:
            restore_note(note_id)
            return True


def export_note_prompt(note_id):
    import os

    from .db.notes import get_note_title
    from .logs import ExportNoteLogs
    from .logs.error import error_print
    from .logs.messages import file_not_found_error_message
    from .utils import is_path_writable

    logs = ExportNoteLogs()
    logs.next_log()

    while True:
        entered_path = NoPromptSuffixPrompt.ask(logs.input_prompt, default=".")

        if os.path.isdir(entered_path):
            return os.path.join(entered_path, get_note_title(note_id)[0])
        elif is_path_writable(entered_path):
            return entered_path
        else:
            error_print(file_not_found_error_message.format(path=entered_path))


def default_editor_prompt(input_prompt):
    from rich.prompt import Prompt

    from .utils import executable_exists, find_default_editor_executable

    editor_exists = False
    while not editor_exists:
        new_editor = Prompt.ask(
            input_prompt,
            default=find_default_editor_executable()
        )
        editor_exists = executable_exists(new_editor)

    return new_editor
