import random
from typing import List


def case_alternating(words: List[str]) -> List[str]:
    """
    Set EVERY OTHER word to UPPER case.
    """
    return [word.upper() if i % 2 == 0 else word for i, word in enumerate(case_lower(words))]


def case_upper(words: List[str]) -> List[str]:
    """
    Set ALL words to UPPER case.
    """
    return [w.upper() for w in words]


def case_first_upper(words: List[str]) -> List[str]:
    """
    Set First character of each word to UPPER case.
    """
    return [w.capitalize() for w in words]


def case_lower(words: List[str]) -> List[str]:
    """
    Set ALL words to LOWER case.
    """
    return [w.lower() for w in words]


def case_capitalize(words: List[str]) -> List[str]:
    """
    Set first letter of each words to UPPER case aka Capitalize.
    """
    return [w.capitalize() for w in words]


def case_random(words: List[str], testing: bool = False) -> List[str]:
    """
    Set RANDOM words to UPPER case.
    """

    def make_upper(word: str) -> str:
        """Return 'word.upper()' on a random basis."""
        if testing:
            random.seed(word)

        if random.choice([True, False]):
            return word.upper()
        else:
            return word

    return [make_upper(word) for word in case_lower(words)]
