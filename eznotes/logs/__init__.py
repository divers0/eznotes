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
    def __init__(self):
        self.options_text = [
            "[[green]1[/green]/[green]edit[/green]/[green]e[/green]]",
            "[[green]2[/green]/[green]view[/green]/[green]v[/green]]",
            "[[green]3[green]/[/green]delete[/green]/[green]d[/green]]"
        ]

    def first(self, note_id):
        console.print(f"[bold]What do you want to do with the note [/bold]'{note_id}'?")

    def second(self):
        console.print(
            "\n".join([f"\t{i+1}. {x}" for i, x in enumerate(self.options_text)])
        )

    def input_prompt(self, note_id):
        # return "|".join([self.options_text[0][:-1]]+list(map(lambda x: x[1:-1:], self.options_text[1:-1:]))+[self.options_text[-1][1:]])
        # this returns
        # [1/edit/e|2/view/v|3/delete/d]
        return f"[bold]\[[green]{note_id}[/]][/]"


class NoPromptSuffixPrompt(Prompt):
    prompt_suffix = " > "


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