import glob
import re
from typing import Iterable, Generator, List, Tuple

# regex representing punctuation that ends a sentence
_SENTENCE_SPLIT_RE = re.compile(
    r"""
        (?<=\w)             # require a word char before our punctuation
        (?:[!?]+|\.)        # split on any number of '?' or '!', or exactly one '.' ...
        (?: |$)             # ...followed by a space or an end-of-line
    """,
    re.X,
)
# regex representing non-word chars at the beginning or end of a word
_WORD_LEADING_TRAINING_PUNC_RE = re.compile(r"(?:^\W+|\W+$)")


def get_sentences_from_lines(line_iterable: Iterable[str]) -> Generator[str, None, None]:
    """Reads a document line by line, and returns a generator of sentences (without end punctuation).
    
    Sentences can span multiple lines - if they do, the sentence will only be returned when ending punctuation is
    seen.
    
    When the end of the iterable is reached, the remaining text will be yielded, even if there is no punctuation
    at the end. Whitespace will be stripped from each yielded sentence. Only non-empty sentences will be yielded.
    
    :param line_iterable:  An iterable containing lines from a file.
    """
    buf = ""
    for line in line_iterable:
        buf += line.strip() + " "
        sentences = _SENTENCE_SPLIT_RE.split(buf)
        for sentence in sentences[:-1]:
            yield sentence.strip()
        buf = sentences[-1]

    stripped_remaining_buf = buf.strip()
    if stripped_remaining_buf:
        yield stripped_remaining_buf


def get_words_from_sentence(sentence: str) -> List[str]:
    """Given a sentence, returns a list of individual words in that sentence.
    
    Words will have leading and trailing punctuation removed, and be converted to lower-case. Only non-empty words
    will be returned.
    
    :param sentence: The sentence to pull words out of
    :returns: A list of all words, normalized to lowercase and with leading and training punctuation removed
    """
    words = sentence.split(" ")
    normalized_words = [_WORD_LEADING_TRAINING_PUNC_RE.sub("", word).lower() for word in words]
    return [word for word in normalized_words if word]


def get_sentences_and_files(file_list: List[str]) -> List[Tuple[str, str]]:
    """Get a list of tuples containing each sentence from each given file, and the corresponding file.
    
    Files are assumed to be .txt files.
    
    :param file_list: A list of file paths to read
    :return: A List of Tuples. Each Tuple contains (sentence, source_file_path).
    """
    sentences = []
    for source_file in file_list:
        with open(source_file, "r", encoding="utf-8") as read_source_file:
            for sentence in get_sentences_from_lines(read_source_file):
                sentences.append((sentence, source_file))
    return sentences


def get_sentences_from_file_glob(file_globs: List[str]) -> List[Tuple[str, str]]:
    """Get a list of tuples containing each sentence (and matching file) from each file matching the given file glob.
    
    :param file_globs: A list of shell-style file glob describing files to read.
    :return: A List of Tuples. Each Tuple contains (sentence, source_file_path).
    """
    matched_files = [matched_file for one_glob in file_globs for matched_file in glob.glob(one_glob)]
    return get_sentences_and_files(matched_files)