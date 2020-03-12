import json
import unittest

from document_parser import WordResult
from document_parser.outputs.json import JsonOutput


class JsonOutputTest(unittest.TestCase):
    def test_returns_correct_output_for_list(self):
        test_output = [
            WordResult(word="a", count=10, sentences={"1", "2"}, files={"a.txt", "b.txt"}),
            WordResult(word="b", count=5, sentences={"3"}, files={"b.txt"}),
        ]

        results = JsonOutput().render(test_output)
        self.assertEqual(
            {
                "words": [
                    {"word": "a", "occurrences": 10, "sentences": ["1", "2"], "files": ["a.txt", "b.txt"]},
                    {"word": "b", "occurrences": 5, "sentences": ["3"], "files": ["b.txt"]},
                ]
            },
            json.loads(results),
        )

    def test_returns_correct_output_for_empty_list(self):
        results = JsonOutput().render([])

        self.assertEqual({"words": []}, json.loads(results))
