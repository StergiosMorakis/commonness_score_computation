from REL.pem_indexers.pem_indexer_base import PemIndexerBase
from urllib.parse import unquote
import json

class WikiPemIndexer(PemIndexerBase):
	'''
		Class responsible for computing P( entity | mention ) using REL's customised WikiExtractor's generated files, once applied on a wikidump.
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

		def _extract_link_info(document: str) -> tuple:
			'''			
				Desc:
					for each document:
						for each hyperlink:
							use text as mention
							use href as entity
							if entity exists in KB:
								create mention - entity pair
				Link example:
					... <a href="
						%CE%BD%CE%B5%CE%BF%CE%B3%CE%BF%CF%84%CE%B8%CE%B9%CE%BA%CE%AE%20%CE%B1%CF%81%CF%87%CE%B9%CF%84%CE%B5%CE%BA%CF%84%CE%BF%CE%BD%CE%B9%CE%BA%CE%AE
					">ανανεωμένο ενδιαφέρο</a> ...
					where:
						entity: %CE%BD%CE%B5%CE%BF%CE%B3%CE%BF%CF%84%CE%B8%CE%B9%CE%BA%CE%AE%20%CE%B1%CF%81%CF%87%CE%B9%CF%84%CE%B5%CE%BA%CF%84%CE%BF%CE%BD%CE%B9%CE%BA%CE%AE
						mention: ανανεωμένο ενδιαφέρο
				Return:
					tuple(
						list(
							(mention_A: str, entityname_A: str, )
							(mention_B: str, entityname_A: str, )
							...
							(mention_A: str, entityname_B: str, )
						), 
						int(failed_entity_matching_count),
					)
			'''
			mention_entity_pairs, failed_entity_matching_count = [], 0
			# WikiExtractor code: "string.replace('<<', '«').replace('>>', '»')"
			consider_semivalid_format = any(case in document for case in ('«a href="', '</a»'))
			if consider_semivalid_format:
				link_index = min(
					(
						document.find(
							f'{char}a href="'
						) for char in (
							'<', 
							'«',
						)
					),
					key= lambda x: x < 0
				)
			else: 
				link_index = document.find('<a href="')
			while link_index >= 0:
				end_entity_index = document.find('">', link_index)
				if document[link_index] == '«':
					end_mention_index = document.find('</a»', end_entity_index)
				else:
					end_mention_index = document.find('</a>', end_entity_index)
				if end_entity_index == -1 or end_mention_index == -1:
					# invalid document format
					break
				mention = document[
					end_entity_index + len('">') 
					: end_mention_index
				]
				entityname = (
					unquote(
						document[
							link_index + len('<a href="') 
							: end_entity_index
						]
					)
				)
				# Filter w/ KB entities
				entity_token = self._pem_controller.entity_indexer[entityname]
				if entity_token:
					mention_entity_pairs.append(
						(
							mention,
							entity_token
						)
					)
				else:
					failed_entity_matching_count += 1
					# print('Entity not matched: {}\nMention: {}\n'.format(entityname, mention))
				link_index = min(
					(
						document.find(
							f'{char}a href="',
							end_mention_index + len("</a>")
						) for char in (
							'<', 
							'«',
						)
					),
					key= lambda x: x < 0
				) if consider_semivalid_format else document.find(
					'<a href="',
					end_mention_index + len("</a>")
				)
			return mention_entity_pairs, failed_entity_matching_count,

		def _groupby_mention_generator(mention_entity_pairs: list) -> iter:
			'''
				MentionToken object ( aggregated entities incl. ) generator

				Desc:
					for each mention: str, entity: WikipediaEntity in mention-entity pairs:
						(
							if new mention:
								create MentionToken object
						)
						add entity to mention

				Example:
					input:
						(mention_A: str, Entity_A: WikipediaEntity, )
						(mention_B: str, Entity_A: WikipediaEntity, )
						(mention_A: str, Entity_B: WikipediaEntity, )
						(mention_A: str, Entity_A: WikipediaEntity, )
					output:
						yield 0:
							mention_A: MentionToken
								._entities{
									Entity_A: 2,
									Entity_B: 1,
								}
						yield 1:
							mention_B: MentionToken
								._entities{
									Entity_A: 1,
								}
			'''
			mentions = {}
			for mention, entity in mention_entity_pairs:
				if mention.strip():	# not empty after removing spaces
					if mention not in mentions:
						mentions[mention] = self._mention_builder.build_token(mention)
					mentions[mention].add_entities(entity)
			for mention in mentions:
				yield mentions[mention]

		valid_hyperlink_count, invalid_hyperlink_count = 0, 0
		curr_document = []
		folderpath_container = self._datapath / 'text'
		assert folderpath_container.exists(), f'Invalid path: {folderpath_container}'
		print(
			'Parsing extracted wikidump...\n\n' + '-' * 8
		)
		for filepath in folderpath_container.glob('*/*'):
			if filepath.is_file():
				with open(
					filepath,
					'r',
					encoding='utf-8'
				) as f:
					print(f'Parsing file "{filepath.name}"...')
					for enum_line, line in enumerate(f, 1):
						if line.startswith('<doc id="'):
							# line has form:
							# <doc id="{ENTITY_ID}" url="{ENTITY_URL}" title="{ENTITY_NAME}">
							curr_doc_id = int(line[len('<doc id="') : line.find('" ')])
							# print(doc_id)
							continue
						else:
							curr_document.append(line)
						if line.startswith('</doc>'):
							# line has form:
							# </doc>
							mention_entity_pairs, failed_entity_matching_count = _extract_link_info(
								' '.join(curr_document)
							)
							valid_hyperlink_count += len(mention_entity_pairs)
							invalid_hyperlink_count += failed_entity_matching_count
							for mention in _groupby_mention_generator(mention_entity_pairs):
								if mention.text_fragment in self._mentions:
									self._mentions[mention.text_fragment].add_entities(mention)
								else:
									self._mentions[mention.text_fragment] = mention
							curr_document = []
						if enum_line % 500000 == 0:
							print(
								f'\tProcessed "{enum_line}" lines, '
								'valid hyperlinks: "{valid_hyperlink_count}", '
								'failed entity links: "{invalid_hyperlink_count}"'
							)
		print(
			'-' * 8 + '\n\n'
			'Parsed extracted wikidump successfully.\n'
			f'\tTotal valid links: {valid_hyperlink_count}\n'
			f'\tTotal invalid links: {invalid_hyperlink_count}\n'
			'Computing Wikipedia P(e|m) values...'
		)
		self._pem_controller.update_pem(self)

