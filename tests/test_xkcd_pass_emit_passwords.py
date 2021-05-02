import argparse
import io
import sys
import unittest
import unittest.mock as mock

from src.xkcd_pass import xkcd_pass


class TestEmitPasswords(unittest.TestCase):
    """
    Test cases for function `emit_passwords`.
    """

    def shortDescription(self) -> None:
        return None

    def setUp(self) -> None:
        """
        Set up fixtures for this test case.
        """
        self.wordlist_small = xkcd_pass.generate_wordlist(
            wordfile="src/xkcd_pass/static/test_list", valid_chars="[a-z]"
        )

        self.wordlist_small_max_min_length = xkcd_pass.generate_wordlist(
            wordfile="src/xkcd_pass/static/test_list",
            valid_chars="[a-z]",
            min_length=7,
            max_length=6,
        )

        self.options = argparse.Namespace(
            interactive=False,
            numwords=6,
            count=1,
            delimiter="",
            separator="\n",
            no_padding_digits=False,
            padding_digits_num=2,
            case="lower",
            verbose=None,
            testing=False,
        )

        self.stdout_patcher = mock.patch.object(sys, "stdout", new_callable=io.StringIO)

    def test_emits_specified_count_of_passwords(self) -> None:
        """
        Should emit passwords numbering specified `count`.
        """
        self.options.count = 6
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.emit_passwords(wordlist=self.wordlist_small, options=self.options)
        output = mock_stdout.getvalue()
        expected_separator = self.options.separator
        expected_separator_count = self.options.count
        self.assertEqual(output.count(expected_separator), expected_separator_count)

    def test_emits_specified_separator_between_passwords(self) -> None:
        """
        Should emit specified separator text between each password.
        """
        self.options.count = 3
        self.options.separator = "!@#$%"
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.emit_passwords(wordlist=self.wordlist_small, options=self.options)
        output = mock_stdout.getvalue()
        expected_separator = self.options.separator
        expected_separator_count = self.options.count
        self.assertEqual(output.count(expected_separator), expected_separator_count)

    def test_emits_no_separator_when_specified_separator_empty(self) -> None:
        """
        Should emit no separator when empty separator specified.
        """
        self.options.count = 1
        self.options.separator = ""
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.emit_passwords(wordlist=self.wordlist_small, options=self.options)
        output = mock_stdout.getvalue()
        unwanted_separator = "\n"
        self.assertEqual(output.find(unwanted_separator), -1)

    def test_emits_no_digits_when_no_padding_digits_is_true(self) -> None:
        """
        Should emit no digits when no_padding_digits is true.
        """
        self.options.no_padding_digits = True
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.emit_passwords(wordlist=self.wordlist_small, options=self.options)
        output = mock_stdout.getvalue()
        self.assertEqual(any(map(str.isdigit, output)), False)

    def test_max_length_less_than_min_length(self) -> None:
        """
        Should work if max_length is less than min_length by setting max_length to same as min_length.
        """
        self.options.numwords = 3
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.emit_passwords(
                wordlist=self.wordlist_small_max_min_length, options=self.options
            )
        output = mock_stdout.getvalue()
        self.assertEqual(len(output.strip()), 23)

    def test_interactive_accept(self) -> None:
        """
        Test if interactive accept works.
        """
        self.options.testing = True
        self.options.interactive = True
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.emit_passwords(
                wordlist=self.wordlist_small_max_min_length, options=self.options
            )
        output = mock_stdout.getvalue()
        self.assertEqual(len(output.strip()), 124)


if __name__ == "__main__":
    test_cases = [
        TestEmitPasswords,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
