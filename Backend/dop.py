from colorama import Fore, Back, Style, init
from enum import Enum


def Color_Text(color: Enum, text: str) -> str:
    return color + text + Style.RESET_ALL


count = 0


def start_file(name: str):
    pass
    # text = Color_Text(Fore.GREEN, "Start " + name)
    # print(text)


def end_file(name: str):
    pass
    # text = Color_Text(Fore.BLUE, "Finish " + name)
    # print(text)



def test_to_work():
    return 10