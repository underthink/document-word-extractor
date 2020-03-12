from typing import NamedTuple, List, Set


class WordResult(NamedTuple):
    """A tuple representing a 'concrete' word, count, and sets of sentences and files in which that word occurs.
    
    This differs from IndexedWordResult by including the full sentence the word occurs in, rather than just a reference.
    """

    word: str
    count: int
    sentences: Set[str]
    files: Set[str]


class IndexedWordResult(NamedTuple):
    """Tuple representing a word, occurrence count, and list of sentence indexes.
    
    An index is the index of element in a list containing a (sentence, file) tuple.
    """

    word: str
    count: int
    sentence_indexes: List[int]
