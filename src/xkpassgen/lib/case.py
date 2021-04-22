import random


def alternating_case(words):
    """
    Set EVERY OTHER word to UPPER case.
    """
    return [
        word.upper() if i % 2 == 0 else word for i, word in enumerate(lower_case(words))
    ]


def upper_case(words):
    """
    Set ALL words to UPPER case.
    """
    return [w.upper() for w in words]


def first_upper_case(words):
    """
    Set First character of each word to UPPER case.
    """
    return [w.capitalize() for w in words]


def lower_case(words):
    """
    Set ALL words to LOWER case.
    """
    return [w.lower() for w in words]


def capitalize_case(words):
    """
    Set first letter of each words to UPPER case aka Capitalize.
    """
    return [w.capitalize() for w in words]


def random_case(words, testing=False):
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

    return [make_upper(word) for word in lower_case(words)]
