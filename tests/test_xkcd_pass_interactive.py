import argparse
import io
import sys
import unittest
import unittest.mock as mock

from src.xkcd_pass import xkcd_pass

WORDFILE = "src/xkcd_pass/static/eff-long"


class TestInteractiveInitialization(unittest.TestCase):
    """
    Test cases for interactive intialization.
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
            interactive=True,
            numwords=6,
            testing=True,
        )

        self.stdout_patcher = mock.patch.object(sys, "stdout", new_callable=io.StringIO)

    def test_interactive_initialization(self) -> None:
        """
        Should test interactive intialization.
        """
        self.options.testtype = "NumWords"
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.initialize_interactive_run(options=self.options)
        output = mock_stdout.getvalue()
        self.assertEqual(output.strip(), str(2))

    def test_interactive_initialization_default_numwords(self) -> None:
        """
        Should test interactive intialization.
        """
        self.options.testtype = "NumWords0"
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.initialize_interactive_run(options=self.options)
        output = mock_stdout.getvalue()
        self.assertEqual(output.strip(), str(6))

    def test_interactive_initialization_error(self) -> None:
        """
        Should test interactive intialization.
        """
        self.options.testtype = "NumWordsError"
        with self.assertRaises(SystemExit):
            xkcd_pass.initialize_interactive_run(options=self.options)


if __name__ == "__main__":
    test_cases = [
        TestInteractiveInitialization,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
