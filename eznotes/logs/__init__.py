from rich.console import Console


console = Console()


class DefaultEditorLogs:
    def first(self):
        console.print("Please enter the [bold green]name[/bold green] of your [bold blue]default editor[/bold blue] [bold](it can be changed later)[/bold]")

    def input_prompt(self):
        console.print("[bold]Editor[/bold] (leave blank for 'vim'): ", end='')


class DeleteNoteLogs:
    def __init__(self, note_id):
        self.note_id = note_id

    def first(self):
        console.print(f"'{self.note_id}' [bold]first 3 lines:[/bold]")

    def second(self):
        console.print(f"[bold]Are you sure[/bold] you want to [bold red]delete[/bold red] the '{self.note_id}' note? \[y/n] ")


class ListViewLogs:
    def first(self, note_id):
        console.print(f"[bold]What do you want to do with the note [/bold]'{note_id}'?")

    def second(self):
        text = """1. [[green]1[/green]/[green]edit[/green]/[green]e[/green]]
        2. [[green]2[/green]/[green]view[/green]/[green]v[/green]]
        3. [[green]3[green]/[/green]delete[/green]/[green]d[/green]]"""
        console.print(text)

    def input_prompt(self, note_id):
        console.print(f"[{note_id}] > ", end='')

    def third(self, user_inp):
        from .error import error_print

        error_print(f"'{user_inp}' is not a valid option.")