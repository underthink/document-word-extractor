import unittest

from document_parser import IndexedWordResult, WordResult
from document_parser.word_counter import get_ordered_word_list, summary_result_generator


class WordCounterTest(unittest.TestCase):
    _EXAMPLE_SENTENCES_AND_FILES = sentences_and_files = [("one two three", "a.txt"), ("two", "b.txt")]
    _EXAMPLE_RESULTS_WITH_INDEXES = [
        IndexedWordResult(word="two", count=2, sentence_indexes=[0, 1]),
        IndexedWordResult(word="one", count=1, sentence_indexes=[0]),
        IndexedWordResult(word="three", count=1, sentence_indexes=[0]),
    ]

    def test_counts_words_correctly_from_multiple_files(self):
        results = get_ordered_word_list(WordCounterTest._EXAMPLE_SENTENCES_AND_FILES)

        self.assertEqual(WordCounterTest._EXAMPLE_RESULTS_WITH_INDEXES, results)

    def test_counts_words_correctly_from_empty_list(self):
        results = get_ordered_word_list([])

        self.assertEqual([], results)

    def test_merges_results_correctly(self):
        results = list(
            summary_result_generator(
                WordCounterTest._EXAMPLE_SENTENCES_AND_FILES, WordCounterTest._EXAMPLE_RESULTS_WITH_INDEXES
            )
        )

        self.assertEqual(
            [
                WordResult(word="two", count=2, sentences={"one two three", "two"}, files={"a.txt", "b.txt"}),
                WordResult(word="one", count=1, sentences={"one two three"}, files={"a.txt"}),
                WordResult(word="three", count=1, sentences={"one two three"}, files={"a.txt"}),
            ],
            results,
        )

    def test_limit_is_respected_if_set(self):
        results = list(
            summary_result_generator(
                WordCounterTest._EXAMPLE_SENTENCES_AND_FILES, WordCounterTest._EXAMPLE_RESULTS_WITH_INDEXES, limit=1
            )
        )

        self.assertEqual(
            [WordResult(word="two", count=2, sentences={"one two three", "two"}, files={"a.txt", "b.txt"})], results
        )
