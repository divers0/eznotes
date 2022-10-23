from rich.console import Console
from rich.prompt import Prompt

from ..utils import text_is_markdown

console = Console()


class DefaultEditorLogs:
    def first(self):
        console.print(
            "Please enter the [bold green]name[/bold green] of your [bold blue]"
            "default editor[/bold blue] [bold](it can be changed later)[/bold]"
        )

    def input_prompt(self):
        return "[bold]Editor[/bold] (leave blank for 'vim'): "


class DeleteNoteLogs:
    def __init__(self, note_id):
        self.note_id = note_id

    def title(self):
        return f"[green]'{self.note_id}'[/] [bold]first 3 lines:[/bold]"

    def input_prompt(self):
        return ("[bold]Are you sure[/bold] you want to [bold red]delete[/bold red]"
        f" the [green]'{self.note_id}'[/green] note?")


class ListViewLogs:
    def __init__(self, options):
        self.options_text = [options_color_coded_text(x) for x in options]

    def first(self, note_id):
        console.print(f"[bold]What do you want to do with the note '{note_id}'?")

    def second(self):
        console.print(
            "\n".join([f"\t{i+1}. {x}" for i, x in enumerate(self.options_text)])
        )

    def input_prompt(self, note_id):
        # return "|".join([self.options_text[0][:-1]]+list(map(lambda x: x[1:-1:], self.options_text[1:-1:]))+[self.options_text[-1][1:]])
        # this returns
        # [1/edit/e|2/view/v|3/delete/d]
        return f"[bold]\[[green]{note_id}[/]][/]"


class ExportNoteLogs:
    def first(self):
        console.print("[bold][green]Where[/green] do you want the [green]note[/green] to be [green]saved[/green]?")

    def input_prompt(self):
        return "[bold blue]Where?[/bold blue]"


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
