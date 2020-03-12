import argparse
import enum

from stop_words import get_stop_words

from document_parser.word_counter import get_ordered_word_list, summary_result_generator
from document_parser.outputs.json import JsonOutput
from document_parser.outputs.table import ConsoleTableOutput
from document_parser.word_extractor import get_sentences_from_file_glob


class OutputTypes(enum.Enum):
    """Possible formats we can output"""
    JSON = JsonOutput()
    TABLE = ConsoleTableOutput()


def parse_args():
    """Parse the args given on the command line, and return the results"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file_glob", help="Shell-style glob specifying the .txt files we should try to parse", nargs="+"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output format",
        default=OutputTypes.TABLE.name,
        choices=[l.lower() for l in OutputTypes.__members__.keys()],
    )
    parser.add_argument("--stop-word-language", "-s", help="Language to use for stop words.", default="en")
    size_group = parser.add_mutually_exclusive_group()
    size_group.add_argument("--limit", "-l", help="Number of rows to generate", type=int, default=10)
    size_group.add_argument("--all", "-a", help="Return all rows. Overrides --limit.", action="store_true")
    return parser.parse_args()


def run_cli_program():
    """Actually run the parser - grab args, extract words and sentences, and print the results to stdout"""
    args = parse_args()
    renderer = OutputTypes[args.output.upper()].value
    stop_words = get_stop_words(args.stop_word_language)
    files_and_sentences = get_sentences_from_file_glob(args.file_glob)
    word_counts = get_ordered_word_list(files_and_sentences, stop_words)
    row_limit = None if args.all else args.limit
    row_result_generator = summary_result_generator(files_and_sentences, word_counts, row_limit)

    print(renderer.render(row_result_generator))
