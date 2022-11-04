def empty_trash(print_done=True):
    from rich.console import Console
    from rich.prompt import Confirm

    from .db.trash import empty_trash, get_trash_notes, trash_is_empty
    from .exceptions import TrashIsAlreadyEmpty
    from .logs import EmptyTrashLogs, done_log

    if trash_is_empty():
        raise TrashIsAlreadyEmpty

    logs = EmptyTrashLogs()
    logs.next_log()

    console = Console()

    notes = "\n".join(
        f"\t[bold blue]{x[0]}[/] - [green]{x[1]}[/]"
        for x in get_trash_notes("alphabetical", "ASC")
    )

    console.print(notes)

    if Confirm.ask(logs.input_prompt):
        empty_trash()
        if print_done:
            done_log()
        return True
    return False


def trash_is_on():
    from .config import get_value_from_config_file
    return get_value_from_config_file("trash")


def turn_trash(on_or_off):
    from .config import change_value_in_conf
    from .db.trash import trash_is_empty
    from .logs import done_log

    trash_was_emptied = True
    if on_or_off == "off" and not trash_is_empty():
        from .logs import TurnTrashOffLogs

        logs = TurnTrashOffLogs()
        logs.next_log()

        trash_was_emptied = empty_trash(False)

    if trash_was_emptied:
        change_value_in_conf("trash", True if on_or_off == "on" else False)
        done_log()
