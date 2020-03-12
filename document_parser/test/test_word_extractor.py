import unittest

from document_parser.word_extractor import get_sentences_from_lines, get_words_from_sentence


class WordExtractorTest(unittest.TestCase):
    def test_yields_correct_sentences_when_given_simple_paragraph(self):
        test_lines = ["This is a sentence. This is also a sentence. Look at all the sentences."]

        results = list(get_sentences_from_lines(test_lines))
        self.assertEqual(["This is a sentence", "This is also a sentence", "Look at all the sentences"], results)

    def test_yields_correct_sentences_when_split_over_several_lines(self):
        test_lines = ["This is a sentence.", "This is ", "also a ", "sentence. Look at all the sentences."]

        results = list(get_sentences_from_lines(test_lines))

        self.assertEqual(["This is a sentence", "This is also a sentence", "Look at all the sentences"], results)

    def test_yields_correct_sentences_when_no_trailing_word_spaces(self):
        test_lines = ["one", "two", "three."]

        results = list(get_sentences_from_lines(test_lines))

        self.assertEqual(["one two three"], results)

    def test_yields_correct_sentences_when_no_periods_on_single_line(self):
        test_lines = ["i am a sentence with no punctuation"]

        results = list(get_sentences_from_lines(test_lines))

        self.assertEqual(["i am a sentence with no punctuation"], results)

    def test_yields_correct_sentences_when_no_periods_on_several_line(self):
        test_lines = ["i", "am ", "a sentence", "with no punctuation"]

        results = list(get_sentences_from_lines(test_lines))

        self.assertEqual(["i am a sentence with no punctuation"], results)

    def test_yields_correct_sentences_when_ends_in_non_period(self):
        test_lines = ["What? A sentence! Will it work?!"]

        results = list(get_sentences_from_lines(test_lines))

        self.assertEqual(["What", "A sentence", "Will it work"], results)

    def test_yields_correct_sentences_when_line_is_empty(self):
        test_lines = [""]

        results = list(get_sentences_from_lines(test_lines))

        self.assertEqual([], results)

    def test_returns_simple_word_list_from_sentence(self):
        results = get_words_from_sentence("i am a sentence")
        self.assertEqual(["i", "am", "a", "sentence"], results)

    def test_returns_correct_words_when_words_have_surrounding_punctuation(self):
        results = get_words_from_sentence('"Foo:" bar?!')
        self.assertEqual(["foo", "bar"], results)

    def test_returns_correct_words_when_words_have_mid_word_punctuation(self):
        results = get_words_from_sentence("don't foo-bar")
        self.assertEqual(["don't", "foo-bar"], results)

    def test_returns_lower_case_words_when_words_have_upper_case(self):
        results = get_words_from_sentence("DON'T SHOUT!")
        self.assertEqual(["don't", "shout"], results)
