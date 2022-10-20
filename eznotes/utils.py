import re


def executable_exists(name):
    from shutil import which

    return which(name) is not None


# this function can be imporved so much over time
# it could have improved a lot right now if i knew more regex but unfortunately
# my regex knowledge ends here.
def text_is_markdown(text):
    if any(1 for _ in re.findall("\*\*[a-zA-Z0-9].*\*\*", text)):
        return True
    if any(1 for _ in re.findall("_[a-zA-Z0-9].*_", text)):
        return True
    for i in text.split('\n'):
        if i.startswith(('# ', '- ', ' - ', '1. ')):
            return True
    return False


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
        from rich.console import Console
        console = Console(color_system='standard')
        console.print(md)
    else:
        return md
