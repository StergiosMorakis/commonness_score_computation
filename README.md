## P(E|M)

***

A project for computing the probability of a Wikipedia entity given a mention.

***

Setup steps:
1. Download desired edition and version of a [`wikidump`](https://dumps.wikimedia.org/elwiki/)
	+ such as, "elwiki-latest-pages-articles-multistream.xml.bz2"
1. Create folder *X/* and append its path to [`config`](EL/config.py) 's datapaths.
1. Run custom [`WikiExtractor`](EL/helper_scripts/wiki_extractor/WikiExtractor.py) and move all generated files to *X/Wikipedia/wiki_version/*
	+ In our example, the *wiki_version* variable is "elwiki-latest"
	+ For instance, run as: `/EL/helper_scripts/wiki_extractor/python WikiExtractor.py ./wiki_corpus.xml --links --filter_disambig_pages --processes 1 --bytes 1G`