import argparse
import io
import os
import sys
import unittest
import unittest.mock as mock

from src.xkcd_pass import xkcd_pass
from xkcd_pass.lib.xkcd_default import DEFAULT_WORDFILE


class TestValidateOptions(unittest.TestCase):
    """
    Test cases for function `validate_options`.
    """

    def shortDescription(self) -> None:
        return None

    def setUp(self) -> None:
        """
        Set up fixtures for this test case.
        """
        self.wordlist_small = xkcd_pass.generate_wordlist(
            wordfile="test_list", 
            min_length=5,
            max_length=9,
            valid_chars="[a-z]"
        )

        self.options_incorrect_length = argparse.Namespace(
            wordfile="test_list", 
            min_length=7,
            max_length=6,
            valid_chars="[a-z]"
        )

        self.options_incorrect_wordfile = argparse.Namespace(
            wordfile="test_list2", 
            min_length=7,
            max_length=7,
            valid_chars="[a-z]"
        )

        self.options_default_wordfile = argparse.Namespace(
            max_length=7,
            min_length=7,
            wordfile=None
        )

        self.stdout_patcher = mock.patch.object(sys, "stdout", new_callable=io.StringIO)

    def test_validate_options_incorrect_length(self) -> None:
        """
        Testing validate options incorrect length.
        """
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.validate_options(options=self.options_incorrect_length)
        output = mock_stdout.getvalue()
        self.assertEqual(len(output.strip()), 81)

    def test_validate_options_incorrect_wordfile(self) -> None:
        """
        Testing validate options incorrect wordfile.
        """
        with self.assertRaises(SystemExit):
            xkcd_pass.validate_options(options=self.options_incorrect_wordfile)

    def test_validate_options_default_wordfile(self) -> None:
        """
        Testing validate options default_wordfile.
        """
        xkcd_pass.DEFAULT_WORDFILE = DEFAULT_WORDFILE
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.validate_options(
                options=self.options_default_wordfile,
                testing=True,
            )
        output = mock_stdout.getvalue()
        self.assertEqual(output.strip(), os.path.abspath("src/xkcd_pass/static/eff-long".strip()))


if __name__ == "__main__":
    test_cases = [
        TestValidateOptions,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
