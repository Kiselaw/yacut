import random

from .constants import LENGTH, SYMBOLS
from .models import URL_map


def get_random_string():
    short = ''.join(random.choice(SYMBOLS) for _ in range(LENGTH))
    while URL_map.query.filter_by(short=short).first():
        short = ''.join(random.choice(SYMBOLS) for _ in range(LENGTH))
    return short
