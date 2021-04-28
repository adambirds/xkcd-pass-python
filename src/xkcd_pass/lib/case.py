import random


def case_alternating(words):
    """
    Set EVERY OTHER word to UPPER case.
    """
    return [
        word.upper() if i % 2 == 0 else word for i, word in enumerate(case_lower(words))
    ]


def case_upper(words):
    """
    Set ALL words to UPPER case.
    """
    return [w.upper() for w in words]


def case_first_upper(words):
    """
    Set First character of each word to UPPER case.
    """
    return [w.capitalize() for w in words]


def case_lower(words):
    """
    Set ALL words to LOWER case.
    """
    return [w.lower() for w in words]


def case_capitalize(words):
    """
    Set first letter of each words to UPPER case aka Capitalize.
    """
    return [w.capitalize() for w in words]


def case_random(words, testing=False):
    """
    Set RANDOM words to UPPER case.
    """

    def make_upper(word):
        """Return 'word.upper()' on a random basis."""
        if testing:
            random.seed(word)

        if random.choice([True, False]):
            return word.upper()
        else:
            return word

    return [make_upper(word) for word in case_lower(words)]
