import io
import sys
import unittest
import unittest.mock as mock

from src.xkcd_pass import xkcd_pass


class TestMain(unittest.TestCase):
    """
    Test cases for function `main`.
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

        self.args = [
            "--min=6",
            "--max=6",
            "-n=3",
        ]

        self.stdout_patcher = mock.patch.object(sys, "stdout", new_callable=io.StringIO)

    def test_main(self) -> None:
        """
        Test main function.
        """
        xkcd_pass.DEFAULT_WORDFILE = "test_list"
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_pass.main()
        output = mock_stdout.getvalue()
        self.assertEqual(len(output.strip()), 20)

    def test_main_verbose(self) -> None:
        """
        Test main function.
        """
        xkcd_pass.DEFAULT_WORDFILE = "test_list"
        self.args.append("-V")
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_pass.main()
        output = mock_stdout.getvalue()
        self.assertEqual(len(output.strip()), 199)

    def test_main_interactive(self) -> None:
        """
        Test main interactive.
        """

        sys.stdin = open("src/xkcd_pass/static/test_files/stdin_main_interactive", "r")

        xkcd_pass.DEFAULT_WORDFILE = "test_list"
        self.args.append("-i")
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_pass.main()
        output = mock_stdout.getvalue()
        self.assertEqual(len(output.strip()), 132)

    def test_main_systemexit(self) -> None:
        """
        Test main interactive error.
        """
        expected_output = "Could not find a word file, or word file does not exist.".strip()

        xkcd_pass.DEFAULT_WORDFILE = "test_list2"
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_pass.main()
        output = mock_stdout.getvalue()
        self.assertEqual(output.strip(), expected_output)

        sys.stdin = sys.__stdin__

    xkcd_pass.DEFAULT_WORDFILE = "eff-long"


if __name__ == "__main__":
    test_cases = [
        TestMain,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
