# Document Word Extraction Exercise

This is a small program to extract words from a set of text documents, count word occurrences,
and print a summary of the top words in a handy and stylish table format (or JSON).



## Running It

This project requires Python 3.5 or later (primarily because of type annotations).

First, set up a virtual environment and install the required modules:

```bash
$ python3 -mvenv parser_venv
$ source parser_venv/bin/activate
$ pip install -r requirements.txt
```

Then (with the virtualenv active) to count the words, returning the top 10 words for all documents
matching a glob:

```bash
$ python -m document_parser "test docs/*.txt"
```

To output as a json document:

```bash
$ python -m document_parser -o json "test docs/*.txt"
```

To return every result (not just the top 10):

```bash
$ python -m document_parser -a "test docs/*.txt"
```

You can also run `python setup.py install` to install the program as a binary 
named `document_parser` - you can then use it directly from the command line
as `document_parser ~/Downloads/test\ docs/*`.

# Todo

See [TODO.md](TODO.md) for limitations and things I ran out of time to do...