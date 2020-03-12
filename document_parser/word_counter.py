import collections
from typing import List, Tuple, Iterable, Generator, Dict

from document_parser import IndexedWordResult, WordResult
from document_parser.word_extractor import get_words_from_sentence


def get_ordered_word_list(
    sentences_and_files: List[Tuple[str, str]], stop_words: Iterable[str] = None
) -> List[IndexedWordResult]:
    """Get a list of tuples containing word, count-of-word, and index-of-sentence-the-word-occurs-in, ordered by count.
    
    The index returned corresponds to the index position of a sentence/filepath in sentences_and_files param we're
    scanning.
    
    :param sentences_and_files: List of Tuples of (sentence, filepath). The sentence in the tuple will be scanned
    for words.
    :param stop_words: A list of stop words to exclude from the results. If not given, no stop words are used.
    
    :return: A list of `IndexedWordResult`s, representing each word in the given sentence set.
    """
    word_counts: Dict[str, int] = collections.defaultdict(lambda: 0)
    word_locations = collections.defaultdict(lambda: [])
    stop_words = set(stop_words) if stop_words else set()

    for sentence_index in range(0, len(sentences_and_files)):
        sentence, _ = sentences_and_files[sentence_index]
        for word in get_words_from_sentence(sentence):
            if word in stop_words:
                continue
            word_counts[word] += 1
            word_locations[word].append(sentence_index)

    sorted_results = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
    return [
        IndexedWordResult(word=this_word, count=word_occurrences, sentence_indexes=word_locations[this_word])
        for this_word, word_occurrences in sorted_results
    ]


def summary_result_generator(
    sentences_and_files: List[Tuple[str, str]], word_occurrences: List[IndexedWordResult], limit: int = None
) -> Generator[WordResult, None, None]:
    """
    A generator that produces concrete WordResult tuples, from a list of indirect IndexedWordResults and the
    source list of sentences and locations.
    
    :param sentences_and_files: List of Tuples of (sentence, filepath). These will be used to get the original
    concrete sentence and file path the word occurred in.
    :param word_occurrences: A list of `IndexedWordResult`s, representing each word in the given sentence set.
    :param limit: The maximum number of results to return. If None, there is no limit.
    :return: A generator that produces a concrete WordResult for each matched word.
    """
    seen = 0
    for occurrence in word_occurrences:
        if seen == limit:
            return
        seen += 1
        files = set()
        sentences = set()
        for location_index in occurrence.sentence_indexes:
            sentences.add(sentences_and_files[location_index][0])
            files.add(sentences_and_files[location_index][1])
        yield WordResult(occurrence.word, occurrence.count, sentences, files)
