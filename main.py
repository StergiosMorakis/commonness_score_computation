from REL.config import config_settings
from REL.entity_indexers.wiki_entity_indexer import WikiEntityIndexer
from REL.pem_indexers.wiki_pem_indexer import WikiPemIndexer
from REL.pem_indexers.yago_pem_indexer import YagoPemIndexer
from REL.pem_indexers.pem_controller import PemController
from pathlib import Path

if __name__ == '__main__':
	datapath = Path(config_settings['datapath'])
	wikipedia_version = 'elwiki-latest'
	wikipedia_path = datapath / 'wikipedia' / wikipedia_version
	assert wikipedia_path.exists(), f'Invalid Path for wiki version {wikipedia_version}'
	# yago_path = datapath / 'yago'

	knowledge_base_entities = WikiEntityIndexer(
		wikipedia_path
	).build_entity_index()

	pem_controller = PemController(knowledge_base_entities, datapath)
	pem_indexers = [
		WikiPemIndexer(wikipedia_path)
		# , YagoPemIndexer(yago_path)
	]
	pem_controller.attach(pem_indexers).build_pem_index()

	# Example Test Case P(E|M) index:
	# key = 'Ηνωμένο Βασίλειο'
	# print(f'\nTest case:\n\t"{key}"')
	# print(pem_controller._pem[key])

	# Uncomment following line to store pem index in DB (TODO):
	# pem_controller.store()
