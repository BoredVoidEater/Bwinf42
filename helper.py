import os
import click
import PIL.Image as Image


def get_user_input(examples_file_name: str, executor_path: str) -> tuple[bool, int]:
    """ließt den User Input ein

    :returns: ob die eigenen Beispiele getestet werden sollen und wie viele Beispiele getestet werden sollen
    """
    # User Input
    own_examples = click.confirm(
        "Sollen die eigenen Beispiele getestet werden?"
    )  # True for own examples, False for the ones from the BwInf

    num_examples = 1

    max_examples = (
        len([name for name in os.listdir(executor_path) if examples_file_name + "Self" in name])
        if own_examples
        else len([name for name in os.listdir(executor_path) if examples_file_name in name and "Self" not in name])
    )

    if click.confirm("Sollen alle Beispiele dieser Kategorie getestet werden?", default=True):
        num_examples = max_examples
    else:
        num_examples = int(
            click.prompt(f"Wie viele Beispiele sollen getestet werden? (maximal {max_examples})", default=1)
        )
    return own_examples, num_examples


def get_example_image(path: str, executor_path: str) -> Image:
    """ließt das Beispiel Bild als png am relativen Pfand ein

    :param path: Der relative pfad von dem Bild des Beispiels
    :returns: ein PIL Image Objekt mit dem Bild des Beispiels
    """
    return Image.open(os.path.join(executor_path, path)).convert("RGB")


def get_example_txt(path: str, executor_path: str) -> list[str]:
    """ließt das Beispiel am relativen Pfand ein

    :param path: Der relative pfad von der txt-Datei des Beispiels
    :returns: eine liste von Zeilen des Beispiels
    """
    return [line.strip() for line in open(os.path.join(executor_path, path)).readlines()]
