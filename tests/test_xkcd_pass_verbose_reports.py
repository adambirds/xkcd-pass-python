import argparse
import io
import sys
import unittest
import unittest.mock as mock

from src.xkcd_pass import xkcd_pass

WORDFILE = "src/xkcd_pass/static/eff-long"


class TestVerboseReports(unittest.TestCase):
    """
    Test cases for function `verbose_reports`.
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

        self.options = argparse.Namespace(
            numwords=6,
            verbose=None,
        )

        self.stdout_patcher = mock.patch.object(sys, "stdout", new_callable=io.StringIO)

    def test_verbose_output(self) -> None:
        """
        Should display verbose reporting.
        """
        self.options.verbose = True
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.verbose_reports(wordlist=self.wordlist_small, options=self.options)
        output = mock_stdout.getvalue()
        expected_output = """
With the current options, your word list contains 6 words.
A 6 word password from this list will have roughly 15 (2.58 * 6) bits of entropy,
assuming truly random word selection.
""".strip()
        self.assertEqual(output.strip(), expected_output)


if __name__ == "__main__":
    test_cases = [
        TestVerboseReports,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
