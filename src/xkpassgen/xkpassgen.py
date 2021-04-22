#!/usr/bin/env python
# encoding: utf-8

import argparse
import math
import os
import os.path
import random
import re
import sys
from io import open

from lib.case import (alternating_case, capitalize_case, first_upper_case,
                      lower_case, random_case, upper_case)

DEFAULT_WORDFILE = "eff-long"

CASE_METHODS = {
    "alternating": alternating_case,
    "upper": upper_case,
    "lower": lower_case,
    "random": random_case,
    "first": first_upper_case,
    "capitalize": capitalize_case,
}

rng = random.SystemRandom

# Python 3 compatibility
if sys.version_info[0] >= 3:
    raw_input = input
    xrange = range

def validate_options(options):
    """
    Given a parsed collection of options, performs various validation checks.
    """

    if options.max_length < options.min_length:
        sys.stderr.write(
            "Warning: maximum word length less than minimum. "
            "Setting maximum equal to minimum.\n"
        )
        # sys.exit(1)

    wordfile = locate_wordfile(wordfile=options.wordfile)
    if not wordfile:
        sys.stderr.write(
            "Could not find a word file, or word file does " "not exist.\n"
        )
        sys.exit(1)


def locate_wordfile(wordfile=None):
    """
    Locate a wordfile from provided name/path. Return a path to wordfile
    either from static directory, the provided path or use a default.
    """
    common_word_files = []
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

    if wordfile is not None:
        # wordfile can be in static dir or provided as a complete path
        common_word_files.append(os.path.join(static_dir, wordfile))
        common_word_files.append(os.path.expanduser(wordfile))

    common_word_files.extend(
        [
            os.path.join(static_dir, DEFAULT_WORDFILE),
            "/usr/share/cracklib/cracklib-small",
            "/usr/share/dict/cracklib-small",
            "/usr/dict/words",
            "/usr/share/dict/words",
        ]
    )

    for wfile in common_word_files:
        if os.path.isfile(wfile):
            return wfile


def set_case(words, method="lower", testing=False):
    """
    Perform capitalization on some or all of the strings in `words`.
    Default method is "lower".
    Args:
        words (list):   word list generated by `choose_words()` or
                        `find_acrostic()`.
        method (str):   one of {"alternating", "upper", "lower",
                        "random"}.
        testing (bool): only affects method="random".
                        If True: the random seed will be set to each word
                        prior to choosing True or False before setting the
                        case to upper. This way we can test that random is
                        working by giving different word lists.
    """
    if (method == "random") and (testing):
        return random_case(words, testing=True)
    else:
        return CASE_METHODS[method](words)


def generate_wordlist(wordfile=None, min_length=5, max_length=9, valid_chars="."):
    """
    Generate a word list from either a kwarg wordfile, or a system default
    valid_chars is a regular expression match condition (default - all chars)
    """

    # deal with inconsistent min and max, erring toward security
    if min_length > max_length:
        max_length = min_length
    wordfile = locate_wordfile(wordfile)

    words = set()

    regexp = re.compile("^{0}{{{1},{2}}}$".format(valid_chars, min_length, max_length))
    # read words from file into wordlist
    with open(wordfile, encoding="utf-8") as wlf:
        for line in wlf:
            thisword = line.strip()
            if regexp.match(thisword) is not None:
                words.add(thisword)

    return list(words)  # deduplicate, just in case


def verbose_reports(wordlist, options):
    """
    Report entropy metrics based on word list and requested password size"
    """

    length = len(wordlist)
    numwords = options.numwords

    bits = math.log(length, 2)

    print("With the current options, your word list contains {0} words.".format(length))

    print(
        "A {0} word password from this list will have roughly "
        "{1} ({2:.2f} * {3}) bits of entropy,"
        "".format(numwords, int(bits * numwords), bits, numwords)
    )
    print("assuming truly random word selection.\n")


def choose_words(wordlist, numwords):
    """
    Choose numwords randomly from wordlist
    """

    return [rng().choice(wordlist) for i in xrange(numwords)]

def generate_random_padding_numbers(padding_digits_num):
    """
    Get random numbers to append to passphrase
    """
    min = pow(10, padding_digits_num-1)
    max = pow(10, padding_digits_num) - 1
    return rng().randint(a=min, b=max)

def try_input(prompt, validate):
    """
    Suppress stack trace on user cancel and validate input with supplied
    validate callable.
    """

    try:
        answer = raw_input(prompt)
    except (KeyboardInterrupt, EOFError):
        # user cancelled
        print("")
        sys.exit(0)

    # validate input
    return validate(answer)


def generate_xkpassword(
    wordlist, numwords=6, interactive=False, delimiter=" ", case="lower", padding_digits=False, padding_digits_num=2
):
    """
    Generate an XKCD-style password from the words in wordlist.
    """

    passwd = None

    def gen_passwd():
        words = choose_words(wordlist, numwords)
        if padding_digits:
            padding_numbers = generate_random_padding_numbers(padding_digits_num)
            return delimiter.join(set_case(words, method=case)) + str(padding_numbers)

        return delimiter.join(set_case(words, method=case))

    # useful if driving the logic from other code
    if not interactive:
        return gen_passwd()

    # else, interactive session
    else:
        # define input validators
        def accepted_validator(answer):
            return answer.lower().strip() in ["y", "yes"]

        # generate passwords until the user accepts
        accepted = False

        while not accepted:
            passwd = gen_passwd()
            print("Generated: " + passwd)
            accepted = try_input("Accept? [yN] ", accepted_validator)
            print("accepted", accepted)
        return passwd


def initialize_interactive_run(options):
    def n_words_validator(answer):
        """
        Validate custom number of words input
        """

        if isinstance(answer, str) and len(answer) == 0:
            return options.numwords
        try:
            number = int(answer)
            if number < 1:
                raise ValueError
            return number
        except ValueError:
            sys.stderr.write("Please enter a positive integer\n")
            sys.exit(1)

    if not options.acrostic:
        n_words_prompt = "Enter number of words (default {0}):\n".format(
            options.numwords
        )
        options.numwords = try_input(n_words_prompt, n_words_validator)
    else:
        options.numwords = len(options.acrostic)


def emit_passwords(wordlist, options):
    """ Generate the specified number of passwords and output them. """
    count = options.count
    while count > 0:
        print(
            generate_xkpassword(
                wordlist,
                interactive=options.interactive,
                numwords=options.numwords,
                delimiter=options.delimiter,
                case=options.case,
                padding_digits=options.padding_digits,
                padding_digits_num=options.padding_digits_num,
            ),
            end=options.separator,
        )
        count -= 1


class XkPassGenArgumentParser(argparse.ArgumentParser):
    """ Command-line argument parser for this program. """

    def __init__(self, *args, **kwargs):
        super(XkPassGenArgumentParser, self).__init__(*args, **kwargs)

        self._add_arguments()

    def _add_arguments(self):
        """ Add the arguments needed for this program. """
        exclusive_group = self.add_mutually_exclusive_group()
        self.add_argument(
            "-w",
            "--wordfile",
            dest="wordfile",
            default=None,
            metavar="WORDFILE",
            help=(
                "Specify that the file WORDFILE contains the list"
                " of valid words from which to generate passphrases."
                " Provided wordfiles: eff-long (default), eff-short,"
                " eff-special"
            ),
        )
        self.add_argument(
            "--min",
            dest="min_length",
            type=int,
            default=5,
            metavar="MIN_LENGTH",
            help="Generate passphrases containing at least MIN_LENGTH words.",
        )
        self.add_argument(
            "--max",
            dest="max_length",
            type=int,
            default=9,
            metavar="MAX_LENGTH",
            help="Generate passphrases containing at most MAX_LENGTH words.",
        )
        exclusive_group.add_argument(
            "-n",
            "--numwords",
            dest="numwords",
            type=int,
            default=6,
            metavar="NUM_WORDS",
            help="Generate passphrases containing exactly NUM_WORDS words.",
        )
        self.add_argument(
            "--padding-digits",
            action="store_true",
            dest="padding_digits",
            default=False,
            help="Append digits to end of passphrase.",
            required='--padding-digits-num' in sys.argv,
        )
        self.add_argument(
            "--padding-digits-num",
            dest="padding_digits_num",
            type=int,
            default=2,
            metavar="PADDING_DIGITS_NUM",
            help="Length of digits to append to end of passphrase.",
        )
        self.add_argument(
            "-i",
            "--interactive",
            action="store_true",
            dest="interactive",
            default=False,
            help=(
                "Generate and output a passphrase, query the user to"
                " accept it, and loop until one is accepted."
            ),
        )
        self.add_argument(
            "-v",
            "--valid-chars",
            dest="valid_chars",
            default=".",
            metavar="VALID_CHARS",
            help=(
                "Limit passphrases to only include words matching the regex"
                " pattern VALID_CHARS (e.g. '[a-z]')."
            ),
        )
        self.add_argument(
            "-V",
            "--verbose",
            action="store_true",
            dest="verbose",
            default=False,
            help="Report various metrics for given options.",
        )
        self.add_argument(
            "-c",
            "--count",
            dest="count",
            type=int,
            default=1,
            metavar="COUNT",
            help="Generate COUNT passphrases.",
        )
        self.add_argument(
            "-d",
            "--delimiter",
            dest="delimiter",
            default=" ",
            metavar="DELIM",
            help="Separate words within a passphrase with DELIM.",
        )
        self.add_argument(
            "-s",
            "--separator",
            dest="separator",
            default="\n",
            metavar="SEP",
            help="Separate generated passphrases with SEP.",
        )
        self.add_argument(
            "-C",
            "--case",
            dest="case",
            type=str,
            metavar="CASE",
            choices=list(CASE_METHODS.keys()),
            default="lower",
            help=(
                "Choose the method for setting the case of each word "
                "in the passphrase. "
                "Choices: {cap_meths} (default: 'lower').".format(
                    cap_meths=list(CASE_METHODS.keys())
                )
            ),
        )


def main(argv=None):
    """ Mainline code for this program. """

    if argv is None:
        argv = sys.argv

    exit_status = 0

    try:
        program_name = os.path.basename(argv[0])
        parser = XkPassGenArgumentParser(prog=program_name)

        options = parser.parse_args(argv[1:])
        validate_options(options)

        my_wordlist = generate_wordlist(
            wordfile=options.wordfile,
            min_length=options.min_length,
            max_length=options.max_length,
            valid_chars=options.valid_chars,
        )

        if options.interactive:
            initialize_interactive_run(options)

        if options.verbose:
            verbose_reports(my_wordlist, options)

        emit_passwords(my_wordlist, options)

    except SystemExit as exc:
        exit_status = exc.code

    return exit_status


if __name__ == "__main__":
    exit_status = main(sys.argv)
    sys.exit(exit_status)
