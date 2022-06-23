from random import choice
from string import ascii_letters, digits


def generate_id(len: int = 16) -> str:
    return "".join([choice(ascii_letters + digits) for _ in range(16)])
