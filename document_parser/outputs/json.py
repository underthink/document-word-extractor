import json
from typing import Generator

from document_parser import WordResult


class JsonOutput:
    """Simple JSON row generator.
    
    Returns an object with a single key, 'words', containing a list of word objects.
    """

    def _generate_json_row(self, row_generator: Generator[WordResult, None, None]):
        for result in row_generator:
            yield {
                "word": result.word,
                "occurrences": result.count,
                "files": sorted(result.files),
                "sentences": sorted(result.sentences),
            }

    def render(self, row_generator) -> str:
        return json.dumps({"words": list(self._generate_json_row(row_generator))})
