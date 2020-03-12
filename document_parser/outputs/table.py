import os
from typing import Generator, Tuple

import texttable

from document_parser import WordResult


class ConsoleTableOutput:
    """Output format that generates a console-friendly table of word counts.
    
    Output table includes a header. The columns included are the word/occurrence count, documents in which
    the word occurs, and sentences that include the word.
    """

    def _generate_table_rows(self, row_generator: Generator[WordResult, None, None]) -> Generator[Tuple[str, str, str], None, None]:
        """Generates a tuple for rendering into a table, containing words, occurrences and locations
        """
        for single_result in row_generator:
            yield (
                "{} ({})".format(single_result.word, single_result.count),
                ", ".join(sorted(single_result.files)),
                "\n\n".join(sorted(single_result.sentences)),
            )

    def _get_terminal_width(self):
        try:
            return os.get_terminal_size()[0]
        except OSError:
            # can't get the terminal size; return a default
            return 80

    def render(self, word_row_generator) -> str:
        # try and use all of the terminal, if possible
        tt = texttable.Texttable(max_width=self._get_terminal_width())
        tt.header(["Word (Total Occurrences)", "Documents", "Sentences containing the word"])
        tt.add_rows(self._generate_table_rows(word_row_generator), header=False)
        return tt.draw()
