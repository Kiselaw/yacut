import random

from .constants import LENGTH, SYMBOLS


def get_random_string():
    return ''.join(random.choice(SYMBOLS) for _ in range(LENGTH))
