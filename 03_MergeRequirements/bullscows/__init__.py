import textdistance as td
from typing import Tuple, List
import random as r


__all__ = ["bullscows", "gameplay"]


def bullscows(guess: str, secret: str) -> Tuple[int, int]:
    bulls = td.hamming.similarity(guess, secret)
    cows = td.bag.similarity(guess, secret) - bulls
    return (bulls, cows)


def gameplay(ask: callable, inform: callable, words: List[str]) -> int:
    secret = r.choice(words)

    attempts = 0
    correct_guess = False
    while not correct_guess:
        guess = ask("Введите слово: ", words)
        attempts += 1

        b, c = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", b, c)

        if guess == secret:
            correct_guess = True

    return attempts

