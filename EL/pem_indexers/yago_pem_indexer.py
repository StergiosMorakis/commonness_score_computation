from EL.pem_indexers.pem_indexer_base import PemIndexerBase

class YagoPemIndexer(PemIndexerBase):
	'''
		Class responsible for computing P( entity | mention ) using a yago_means.tsv file.
		That custom file consists of {mention} {wikipedia entity} tab sep columns ([YAGO -> Wikidata -> Wikipedia] entity mapping).
		Subclass of PemIndexerBase and must therefore override PemIndexerBase' abstract build_index() funtion, depending on use-case.
	'''

	def build_pem_index(self):
		'''
			Desc:
				Fill {self._mentions} with str mentions as keys and MentionToken objects as values.
				MentionToken.add_entities() is used for filling mention objects with entities.
				Finally, {self._pem_controller.update_pem(self)} is called for passing control to PemController, 
					an object responsible for handling multiple p(e|m) indexes. (* Observer design pattern)
		'''

		valid_entity_count, invalid_entity_count = 0, 0
		filepath = self._datapath / 'yago_means.tsv'
		with open(
			self._datapath,
			'r',
			encoding='utf-8'
		) as f:
			for enum_line, line in enumerate(f):
				mention, wikipedia_entity = line.strip().split('\t')
				mention = mention[1:-4] # example: '"γαλαξίας"@el'
				# Filter w/ KB entities
				entity_token = self._pem_controller.entity_indexer[wikipedia_entity]
				if entity_token and mention:
					if mention not in self._mentions:
						self._mentions[mention] = self._mention_builder.build_token(mention)
					self._mentions[mention].add_entities(entity_token)
					valid_entity_count += 1
				else:
					invalid_entity_count += 1

			if enum_line % 50000 == 0:
				print(
					f'\tProcessed "{enum_line}" lines, valid hyperlinks: "{valid_entity_count}", failed entity links: "{invalid_entity_count}"'
				)
		print(
			'-' * 8 + '\n\n'
			'Parsed yago_means.tsv file successfully.\n'
			f'\tTotal valid links: {valid_entity_count}\n'
			f'\tTotal invalid links: {invalid_entity_count}\n'
			'Computing YAGO P(e|m) values...'
		)
		self._pem_controller.update_pem(self)
