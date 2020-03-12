# Todo/Current limitations

* More test coverage (in particular in some of the CLI parsing, and some of the functions that deal with IO)
* Some punctuation sequences aren't handled as well as they should be - 'hyphen-[\n]ated' will be be incorrectly 
  considered two distinct words; 'Sentence with... ellipsis' will be considered distinct sentences.
* Usage of `re.split` can be slow for some documents
* Only UTF-8 files are supported
* Doesn't give great feedback if the file glob doesn't match any documents