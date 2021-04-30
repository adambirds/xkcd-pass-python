import re
import unittest

from src.xkcd_pass import xkcd_pass

WORDFILE = "src/xkcd_pass/static/eff-long"


class TestGenerateWordlist(unittest.TestCase):
    """
    Test cases for function `generate_xkpassword`.
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

    def test_delim(self) -> None:
        """
        Test delimiter is set correctly.
        """
        tdelim = "_"
        result = xkcd_pass.generate_xkpassword(self.wordlist_small, delimiter=tdelim)
        self.assertIsNotNone(re.match("([a-zA-z]+(_|)+([0-9])+)+", result))


if __name__ == "__main__":
    test_cases = [
        TestGenerateWordlist,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
