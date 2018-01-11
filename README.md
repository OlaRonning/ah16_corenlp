## CoreNLP pipeline for Dependecies and Lemmas
The included scripts are for interaction with Dustin Smiths [python-wrapper](https://github.com/dasmith/stanford-corenlp-python) for Stanfords CoreNLP.
## Setup
1. Clone the [python wrapper](https://github.com/dasmith/stanford-corenlp-python), and follow the instruction for installation.
2. Copy coreNLP.py and gen_dep_lemma.py to the python wrapper directory

## Parsing examples
Start the coreNLP server:

``` > python2 coreNLP.py &```

Run the gen_dep_lemma.py script:

``` > python2 gen_dep_lemma.py linesWithAnnotations110716.json ```

Dependencies and lemma are written to dep_lemma.jsons

Use dep_lemma.jsons with the -d flag for makeFeats_withCataphora.py
