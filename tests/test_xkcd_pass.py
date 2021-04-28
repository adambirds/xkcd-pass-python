import argparse
import io
import os
import re
import sys
import unittest
import unittest.mock as mock
from subprocess import PIPE, Popen

from src.xkcd_pass import xkcd_pass

WORDFILE = "src/xkcd_pass/static/eff-long"


class xkcd_passTests(unittest.TestCase):
    def shortDescription(self):
        return None

    def setUp(self):
        self.wordlist_full = xkcd_pass.generate_wordlist(
            wordfile=WORDFILE,
            min_length=5,
            max_length=8,
        )
        self.wordlist_small = xkcd_pass.generate_wordlist(
            wordfile="src/xkcd_pass/static/test_list", valid_chars="[a-z]"
        )

    def test_loadwordfile(self):
        """
        Test load wordlist is correct.
        """
        self.assertEqual(len(self.wordlist_full), 5670)

    def test_regex(self):
        """
        Test regex.
        """
        self.assertNotIn("__$$$__", self.wordlist_small)

    def test_delim(self):
        """
        Test delimiter is set correctly.
        """
        tdelim = "_"
        result = xkcd_pass.generate_xkpassword(self.wordlist_small, delimiter=tdelim)
        self.assertIsNotNone(re.match("([a-zA-z]+(_|)+([0-9])+)+", result))

    def test_set_case(self):
        """
        Test set_case works correctly.
        """
        words = "this is only a test".lower().split()
        words_before = set(words)

        results = {}

        results["lower"] = xkcd_pass.set_case(words, method="lower")
        results["upper"] = xkcd_pass.set_case(words, method="upper")
        results["alternating"] = xkcd_pass.set_case(words, method="alternating")
        results["random"] = xkcd_pass.set_case(words, method="random", testing=True)
        results["first"] = xkcd_pass.set_case(words, method="first")
        results["capitalize"] = xkcd_pass.set_case(words, method="capitalize")

        words_after = set(
            word.lower() for group in list(results.values()) for word in group
        )

        # Test that no words have been fundamentally mutated by any of the methods
        self.assertTrue(words_before == words_after)

        # Test that the words have been uppered or lowered respectively.
        self.assertTrue(all(word.islower() for word in results["lower"]))
        self.assertTrue(all(word.isupper() for word in results["upper"]))
        self.assertTrue(all(word.istitle() for word in results["first"]))
        self.assertTrue(all(word.istitle() for word in results["capitalize"]))
        # Test that the words have been correctly uppered randomly.
        expected_random_result_1_py3 = ["THIS", "IS", "ONLY", "a", "test"]
        expected_random_result_2_py3 = ["THIS", "IS", "a", "test", "ALSO"]
        expected_random_result_1_py2 = ["this", "is", "only", "a", "TEST"]
        expected_random_result_2_py2 = ["this", "is", "a", "TEST", "also"]

        words_extra = "this is a test also".lower().split()
        observed_random_result_1 = results["random"]
        observed_random_result_2 = xkcd_pass.set_case(
            words_extra, method="random", testing=True
        )

        self.assertIn(
            observed_random_result_1,
            (expected_random_result_1_py2, expected_random_result_1_py3),
        )
        self.assertIn(
            observed_random_result_2,
            (expected_random_result_2_py2, expected_random_result_2_py3),
        )


class TestInteractiveInitialization(unittest.TestCase):
    """
    Test cases for interactive intialization.
    """

    def shortDescription(self):
        return None

    def setUp(self):
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

    def test_interactive_initialization(self):
        """
        Should test interactive intialization.
        """
        self.options.testtype = "NumWords"
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.initialize_interactive_run(options=self.options)
        output = mock_stdout.getvalue()
        self.assertEqual(output.strip(), str(2))

    def test_interactive_initialization_default_numwords(self):
        """
        Should test interactive intialization.
        """
        self.options.testtype = "NumWords0"
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.initialize_interactive_run(options=self.options)
        output = mock_stdout.getvalue()
        self.assertEqual(output.strip(), str(6))

    def test_interactive_initialization_error(self):
        """
        Should test interactive intialization.
        """
        self.options.testtype = "NumWordsError"
        with self.assertRaises(SystemExit):
            with self.stdout_patcher as mock_stdout:
                xkcd_pass.initialize_interactive_run(options=self.options)


class TestVerboseReports(unittest.TestCase):
    """
    Test cases for function `verbose_reports`.
    """

    def shortDescription(self):
        return None

    def setUp(self):
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

    def test_verbose_output(self):
        """
        Should display verbose reporting.
        """
        self.options.verbose = True
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.verbose_reports(
                wordlist=self.wordlist_small, options=self.options
            )
        output = mock_stdout.getvalue()
        expected_output = """
With the current options, your word list contains 6 words.
A 6 word password from this list will have roughly 15 (2.58 * 6) bits of entropy,
assuming truly random word selection.
""".strip()
        self.assertEqual(output.strip(), expected_output)


class TestEmitPasswords(unittest.TestCase):
    """
    Test cases for function `emit_passwords`.
    """

    def shortDescription(self):
        return None

    def setUp(self):
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
            separator=u"\n",
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

    def test_emits_specified_separator_between_passwords(self):
        """
        Should emit specified separator text between each password.
        """
        self.options.count = 3
        self.options.separator = u"!@#$%"
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.emit_passwords(wordlist=self.wordlist_small, options=self.options)
        output = mock_stdout.getvalue()
        expected_separator = self.options.separator
        expected_separator_count = self.options.count
        self.assertEqual(output.count(expected_separator), expected_separator_count)

    def test_emits_no_separator_when_specified_separator_empty(self):
        """
        Should emit no separator when empty separator specified.
        """
        self.options.count = 1
        self.options.separator = u""
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.emit_passwords(wordlist=self.wordlist_small, options=self.options)
        output = mock_stdout.getvalue()
        unwanted_separator = "\n"
        self.assertEqual(output.find(unwanted_separator), -1)

    def test_emits_no_digits_when_no_padding_digits_is_true(self):
        """
        Should emit no digits when no_padding_digits is true.
        """
        self.options.no_padding_digits = True
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.emit_passwords(wordlist=self.wordlist_small, options=self.options)
        output = mock_stdout.getvalue()
        self.assertEqual(any(map(str.isdigit, output)), False)

    def test_max_length_less_than_min_length(self):
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

    def test_interactive_accept(self):
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
        self.assertEqual(len(output.strip()), 119)


class TestValidateOptions(unittest.TestCase):
    """
    Test cases for function `validate_options`.
    """

    def shortDescription(self):
        return None

    def setUp(self):
        """
        Set up fixtures for this test case.
        """
        self.wordlist_small = xkcd_pass.generate_wordlist(
            wordfile="src/xkcd_pass/static/test_list", valid_chars="[a-z]"
        )

        self.options_incorrect_length = argparse.Namespace(
            max_length=6, min_length=7, wordfile="src/xkcd_pass/static/test_list"
        )

        self.options_incorrect_wordfile = argparse.Namespace(
            max_length=7, min_length=7, wordfile="src/xkcd_pass/static/test_list2"
        )

        self.options_default_wordfile = argparse.Namespace(
            max_length=7,
            min_length=7,
            wordfile=None,
        )

        self.stdout_patcher = mock.patch.object(sys, "stdout", new_callable=io.StringIO)

    def test_validate_options_incorrect_length(self):
        """
        Testing validate options incorrect length.
        """
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.validate_options(options=self.options_incorrect_length)
        output = mock_stdout.getvalue()
        self.assertEqual(len(output.strip()), 81)

    def test_validate_options_incorrect_wordfile(self):
        """
        Testing validate options incorrect wordfile.
        """
        with self.assertRaises(SystemExit):
            with self.stdout_patcher as mock_stdout:
                xkcd_pass.validate_options(options=self.options_incorrect_wordfile)

    def test_validate_options_default_wordfile(self):
        """
        Testing validate options default_wordfile.
        """
        with self.stdout_patcher as mock_stdout:
            xkcd_pass.validate_options(
                options=self.options_default_wordfile,
                testing=True,
            )
        output = mock_stdout.getvalue()
        self.assertEqual(
            output.strip(), os.path.abspath("src/xkcd_pass/static/eff-long".strip())
        )


class TestTryInput(unittest.TestCase):
    """
    Test cases for function `try_input`.
    """

    def shortDescription(self):
        return None

    def setUp(self):
        """
        Set up fixtures for this test case.
        """
        self.prompt = "Accept? [yN] "

        self.stdout_patcher = mock.patch.object(sys, "stdout", new_callable=io.StringIO)

    def test_try_input(self):
        """
        Test try input.
        """

        def accepted_validator(answer):
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

    def test_try_input_failure(self):
        """
        Test try input failure.
        """

        def accepted_validator(answer):
            return answer.lower().strip() in ["y", "yes"]

        sample_input = io.StringIO()
        sys.stdin = sample_input
        sample_input.write("")
        sample_input.seek(0)

        with self.assertRaises(SystemExit):
            output = xkcd_pass.try_input(
                prompt=self.prompt,
                validate=accepted_validator,
                testing=False,
                method=None,
            )

    sys.stdin = sys.__stdin__


class TestMain(unittest.TestCase):
    """
    Test cases for function `main`.
    """

    def shortDescription(self):
        return None

    def setUp(self):
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

    def test_main(self):
        """
        Test main function.
        """
        xkcd_pass.DEFAULT_WORDFILE = "test_list"
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_pass.main()
        output = mock_stdout.getvalue()
        self.assertEqual(len(output.strip()), 20)

    def test_main_verbose(self):
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

    def test_main_interactive(self):
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

    def test_main_systemexit(self):
        """
        Test main interactive error.
        """
        expected_output = (
            "Could not find a word file, or word file does not exist.".strip()
        )

        xkcd_pass.DEFAULT_WORDFILE = "test_list2"
        with mock.patch.object(sys, "argv", self.args):
            with self.stdout_patcher as mock_stdout:
                xkcd_pass.main()
        output = mock_stdout.getvalue()
        self.assertEqual(output.strip(), expected_output)

        sys.stdin = sys.__stdin__


class TestInit(unittest.TestCase):
    """
    Test cases for function `init`.
    """

    def setUp(self):
        """
        Set up fixtures for this test case.
        """

        self.args = [
            "--min=6",
            "--max=6",
            "-n=3",
        ]

    def test_init(self):
        """
        Test init() function.
        """
        with mock.patch.object(sys, "argv", self.args):
            with mock.patch.object(xkcd_pass, "main", return_value=42):
                with mock.patch.object(xkcd_pass, "__name__", "__main__"):
                    with mock.patch.object(xkcd_pass.sys, "exit") as mock_exit:
                        xkcd_pass.init()
                        assert mock_exit.call_args[0][0] == 42


class TestEntropyInformation(unittest.TestCase):
    """
    Test cases for function `emit_passwords`.
    """

    def shortDescription(self):
        return None

    @staticmethod
    # def run_xkcd_pass_process(*args):
    #     process = Popen(["xkcd_pass", "-V", "-i"], stdout=PIPE, stdin=PIPE)
    #     return process.communicate('\n'.join(args))[0]

    @staticmethod
    def test_entropy_printout_valid_input(self):
        values = self.run_xkcd_pass_process("4", "y")
        self.assertIn("A 4 word password from this list will have roughly 51", values)


if __name__ == "__main__":
    test_cases = [
        xkcd_passTests,
        TestInteractiveInitialization,
        TestVerboseReports,
        TestValidateOptions,
        TestTryInput,
        TestInit,
        TestMain,
        TestEmitPasswords,
        TestEntropyInformation,
    ]
    suites = [
        unittest.TestLoader().loadTestsFromTestCase(test_case)
        for test_case in test_cases
    ]
    unittest.TextTestRunner(verbosity=2, buffer=True).run(unittest.TestSuite(suites))
