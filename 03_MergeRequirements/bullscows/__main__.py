from typing import List
import urllib.request
import sys
import os


from . import gameplay


def ask(prompt: str, valid: List[str] = None) -> str:
    while True:
        print(prompt, end="")
        guess = input()

        if (valid is not None) and (guess not in valid):
            continue
        return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


if __name__ == "__main__":
    filename = sys.argv[1]
    if os.path.isfile(filename):
        file = open(filename)
        lines = [line.rstrip() for line in file]
    else:
        response = urllib.request.urlopen(filename)
        html_response = response.read()
        encoding = response.headers.get_content_charset('utf-8')
        lines = html_response.decode(encoding).split()

    if len(sys.argv) > 2:
        length = int(sys.argv[2])
        lines = list(filter(lambda x: len(x) == length, lines))

    print(f"Количество попыток: {gameplay(ask, inform, lines)}")


