import textwrap
import unittest

from document_parser import WordResult
from document_parser.outputs.table import ConsoleTableOutput


class JsonOutputTest(unittest.TestCase):
    def test_returns_correct_output_for_list(self):
        test_output = [
            WordResult(word="a", count=10, sentences={"1", "2"}, files={"a.txt", "b.txt"}),
            WordResult(word="b", count=5, sentences={"3"}, files={"b.txt"}),
        ]

        results = ConsoleTableOutput().render(test_output)

        expected_result = textwrap.dedent(
            """
            +--------------------------+--------------+-------------------------------+
            | Word (Total Occurrences) |  Documents   | Sentences containing the word |
            +==========================+==============+===============================+
            | a (10)                   | a.txt, b.txt | 1                             |
            |                          |              |                               |
            |                          |              | 2                             |
            +--------------------------+--------------+-------------------------------+
            | b (5)                    | b.txt        | 3                             |
            +--------------------------+--------------+-------------------------------+
        """
        )

        self.assertEqual(expected_result.strip(), results.strip())

    def test_returns_correct_output_for_empty_list(self):
        results = ConsoleTableOutput().render([])

        expected_result = textwrap.dedent(
            """
            +--------------------------+-----------+-------------------------------+
            | Word (Total Occurrences) | Documents | Sentences containing the word |
            +==========================+===========+===============================+
            +--------------------------+-----------+-------------------------------+
        """
        )

        self.assertEqual(expected_result.strip(), results.strip())
