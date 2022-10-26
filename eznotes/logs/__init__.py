from rich.console import Console
from rich.prompt import Prompt

from ..utils import text_is_markdown

console = Console()


class Log:
    def __init__(self):
        self.cursor = 0
    def next_log(self, **args):
        console.print(self.logs[self.cursor].format(**args))
        self.cursor += 1


class DefaultEditorLogs(Log):
    def __init__(self):
        super().__init__()
        self.logs = [
            "Please enter the [bold green]name[/bold green] of your [bold blue]"
            "default editor[/bold blue] [bold](it can be changed later)[/bold]"
        ]

        self.input_prompt = "[bold]Editor[/bold]:"


class DeleteNoteLogs(Log):
    def __init__(self, note_id):
        super().__init__()

        self.note_id = note_id
        self.title = f"[green]'{self.note_id}'[/] [bold]first 3 lines:[/bold]"
        self.input_prompt =  (
            "[bold]Are you sure[/bold] you want to [bold red]delete[/bold red]"
            f" the [green]'{self.note_id}'[/green] note?"
        )


class ListViewLogs(Log):
    def __init__(self, options):
        super().__init__()

        self.options_text = [options_color_coded_text(x) for x in options]
        self.logs = [
            "[bold]What do you want to do with the note '{note_id}'?",
            "\n".join([f"\t{i+1}. {x}" for i, x in enumerate(self.options_text)])
        ]


class ExportNoteLogs(Log):
    def __init__(self):
        super().__init__()

        self.logs = [
            "[bold][green]Where[/green] do you want the [green]note[/green] to be [green]saved[/green]?"
        ]

        self.input_prompt = "[bold blue]Where?[/bold blue]"


class NoPromptSuffixPrompt(Prompt):
    prompt_suffix = " "


def done_log():
    console.print("\t[bold green]Done.")


def selected_note_log(note_id):
    console.print(f"[bold]Selected note ID: [green]{note_id}")


def markdown_print(text, print_=True):
    if not text_is_markdown(text):
        if print_:
            print(text)
        else:
            return text
        return
    from rich.markdown import Markdown

    md = Markdown(text)
    if print_:
        console = Console(color_system="standard")
        console.print(md)
    else:
        return md


def pager_view(text):
    with console.pager(styles=True):
        console.print(text)


def panel_print(text, title=None):
    from rich.panel import Panel

    console.print(Panel(text, title=title))


def options_color_coded_text(options):
    return f"[{'/'.join([f'[not bold green]{x}[/not bold green]' for x in options])}]"
