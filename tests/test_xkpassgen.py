from subprocess import PIPE, Popen
import argparse
import io
import re
import sys
import unittest
import unittest.mock as mock


from xkpassgen import xkpassgen


WORDFILE = 'src/xkpassgen/static/eff-long'


class XkPassGenTests(unittest.TestCase):
    def setUp(self):
        self.wordlist_full = xkpassgen.generate_wordlist(
            wordfile=WORDFILE,
            min_length=5,
            max_length=8,)
        self.wordlist_small = xkpassgen.generate_wordlist(
            wordfile='src/xkpassgen/static/test_list',
            valid_chars='[a-z]')

    def test_loadwordfile(self):
        self.assertEqual(len(self.wordlist_full), 5670)

    def test_regex(self):
        self.assertNotIn("__$$$__", self.wordlist_small)

    def test_delim(self):
        tdelim = "_"
        result = xkpassgen.generate_xkpassword(
            self.wordlist_small,
            delimiter=tdelim)
        self.assertIsNotNone(re.match('([a-zA-z]+(_|)+([0-9])+)+', result))

    def test_set_case(self):
        words = "this is only a test".lower().split()
        words_before = set(words)

        results = {}

        results["lower"] = xkpassgen.set_case(words, method="lower")
        results["upper"] = xkpassgen.set_case(words, method="upper")
        results["alternating"] = xkpassgen.set_case(words, method="alternating")
        results["random"] = xkpassgen.set_case(words, method="random", testing=True)
        results["first"] = xkpassgen.set_case(words, method="first")

        words_after = set(word.lower() for group in list(results.values()) for word in group)

        # Test that no words have been fundamentally mutated by any of the methods
        self.assertTrue(words_before == words_after)

        # Test that the words have been uppered or lowered respectively.
        self.assertTrue(all(word.islower() for word in results["lower"]))
        self.assertTrue(all(word.isupper() for word in results["upper"]))
        self.assertTrue(all(word.istitle() for word in results["first"]))
        # Test that the words have been correctly uppered randomly.
        expected_random_result_1_py3 = ['THIS', 'IS', 'ONLY', 'a', 'test']
        expected_random_result_2_py3 = ['THIS', 'IS', 'a', 'test', 'ALSO']
        expected_random_result_1_py2 = ['this', 'is', 'only', 'a', 'TEST']
        expected_random_result_2_py2 = ['this', 'is', 'a', 'TEST', 'also']

        words_extra = "this is a test also".lower().split()
        observed_random_result_1 = results["random"]
        observed_random_result_2 = xkpassgen.set_case(
            words_extra,
            method="random",
            testing=True
        )

        self.assertIn(observed_random_result_1, (expected_random_result_1_py2, expected_random_result_1_py3))
        self.assertIn(observed_random_result_2, (expected_random_result_2_py2, expected_random_result_2_py3))


class TestEmitPasswords(unittest.TestCase):
    """ Test cases for function `emit_passwords`. """

    def setUp(self):
        """ Set up fixtures for this test case. """
        self.wordlist_small = xkpassgen.generate_wordlist(
            wordfile='tests/test_list.txt',
            valid_chars='[a-z]')

        self.options = argparse.Namespace(
            interactive=False,
            numwords=6,
            count=1,
            acrostic=False,
            delimiter=" ",
            separator=u"\n",
            no_padding_digits=False,
            padding_digits_num=2,
            case='lower',
        )

        self.stdout_patcher = mock.patch.object(
            sys, 'stdout', new_callable=io.StringIO)

    def test_emits_specified_count_of_passwords(self) -> None:
        """
        Should emit passwords numbering specified `count`.
        """
        self.options.count = 6
        with self.stdout_patcher as mock_stdout:
            xkpassgen.emit_passwords(
                wordlist=self.wordlist_small,
                options=self.options)
        output = mock_stdout.getvalue()
        expected_separator = self.options.separator
        expected_separator_count = self.options.count
        self.assertEqual(
            output.count(expected_separator), expected_separator_count)

    def test_emits_specified_separator_between_passwords(self):
        """ Should emit specified separator text between each password. """
        self.options.count = 3
        self.options.separator = u"!@#$%"
        with self.stdout_patcher as mock_stdout:
            xkpassgen.emit_passwords(
                wordlist=self.wordlist_small,
                options=self.options)
        output = mock_stdout.getvalue()
        expected_separator = self.options.separator
        expected_separator_count = self.options.count
        self.assertEqual(
            output.count(expected_separator), expected_separator_count)

    def test_emits_no_separator_when_specified_separator_empty(self):
        """ Should emit no separator when empty separator specified. """
        self.options.count = 1
        self.options.separator = u""
        with self.stdout_patcher as mock_stdout:
            xkpassgen.emit_passwords(
                wordlist=self.wordlist_small,
                options=self.options)
        output = mock_stdout.getvalue()
        unwanted_separator = "\n"
        self.assertEqual(output.find(unwanted_separator), -1)


class TestEntropyInformation(unittest.TestCase):
    """ Test cases for function `emit_passwords`. """

    @staticmethod
    # def run_xkcdpass_process(*args):
    #     process = Popen(["xkcdpass", "-V", "-i"], stdout=PIPE, stdin=PIPE)
    #     return process.communicate('\n'.join(args))[0]

    @staticmethod
    def test_entropy_printout_valid_input(self):
        values = self.run_xkpassgen_process('4', 'y')
        self.assertIn('A 4 word password from this list will have roughly 51', values)


if __name__ == '__main__':
    test_cases = [XkPassGenTests, TestEmitPasswords, TestEntropyInformation]
    suites = [unittest.TestLoader().loadTestsFromTestCase(test_case) for test_case in test_cases]
    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(suites))