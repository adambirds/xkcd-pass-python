import io
import sys
import unittest
import unittest.mock as mock

from src.xkcd_pass import xkcd_pass


class TestTryInput(unittest.TestCase):
    """
    Test cases for function `try_input`.
    """

    def shortDescription(self) -> None:
        return None

    def setUp(self) -> None:
        """
        Set up fixtures for this test case.
        """
        self.prompt = "Accept? [yN] "

        self.stdout_patcher = mock.patch.object(sys, "stdout", new_callable=io.StringIO)

    def test_try_input(self) -> None:
        """
        Test try input.
        """

        def accepted_validator(answer: str) -> bool:
            return answer.lower().strip() in ["y", "yes"]

        sample_input = io.StringIO()
        sys.stdin = sample_input
        sample_input.write("y")
        sample_input.seek(0)

        output = xkcd_pass.try_input(
            prompt=self.prompt,
            validate=accepted_validator,
            testing=False,
            method=None,
        )

        self.assertEqual(output, True)

    def test_try_input_failure(self) -> None:
        """
        Test try input failure.
        """

        def accepted_validator(answer: str) -> bool:
            return answer.lower().strip() in ["y", "yes"]

        sample_input = io.StringIO()
        sys.stdin = sample_input
        sample_input.write("")
        sample_input.seek(0)

        with self.assertRaises(SystemExit):
            xkcd_pass.try_input(
                prompt=self.prompt,
                validate=accepted_validator,
                testing=False,
                method=None,
            )

    sys.stdin = sys.__stdin__


if __name__ == "__main__":
    test_cases = [
        TestTryInput,
    ]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
