## P(E|M)

***

A project for computing the probability of an entity given a mention on Wikipedia.

***

Setup steps:
1. Download desired edition and version of a [`wikidump`](https://dumps.wikimedia.org/elwiki/)
	+ example: elwiki-latest-pages-articles-multistream.xml.bz2
1. Create folder *X/* and add its path to [`config`](EL/config.py) 's datapaths.
1. Run custom [`WikiExtractor`](EL/helper_scripts/wiki_extractor/WikiExtractor.py) and add generated files to *X/Wikipedia/wiki_version/* path
	+ In our example, *wiki_version* variable is "elwiki-latest"
	+ `/EL/helper_scripts/wiki_extractor/python WikiExtractor.py ./wiki_corpus.xml --links --filter_disambig_pages --processes 1 --bytes 1G`