from EL.tokens.token_handler_service import TokenHandlerService
from EL.tokens.tokens.wikipedia_token import WikipediaEntity
from EL.entity_indexers.entity_indexer_base import EntityIndexerBase

class WikiEntityIndexer(EntityIndexerBase):
	'''
		Class responsible for loading entities from EL.helper_scripts.wiki_extractor's customised Wikiextractor's (credits to REL) generated files, once applied on a wikidump.
		Subclass of EntityIndexerBase and must therefore override EntityIndexerBase' abstract build_entity_index() funtion, depending on use-case.
	'''

	def __init__(
		self, 
		datapath: object,
	):
		super().__init__(
			datapath
		)
		self._entity_handler = TokenHandlerService(WikipediaEntity)				# (Overrides super()._entity_handler) Used for constructing WikipediaEntity objects 
		self._helper_dicts = {													# Opt. lookup
			'formatted_entitynames': {},										# formatted_entityname as key, WikipediaEntity as value
			'entity_ids': {},													# entityid as key, WikipediaEntity as value
		}

	def _get_redirected_entity(
		self,
		token: WikipediaEntity
	) -> WikipediaEntity:
		''' 
			input:
				source_entity: WikipediaEntity
					( an entity that redirects to another entity via its redirect_to_entityid attribute )
			output:
				target_entity: WikipediaEntity ( its redirect_to_entityid attribute is None )
		'''
		if token:
			while token.redirect_to_entityid in self._helper_dicts['entity_ids']:
				token = self._helper_dicts['entity_ids'][token.redirect_to_entityid]
			return token

	def __getitem__(
		self,
		key: object,
	) -> WikipediaEntity:
		'''
			Return either WikipediaEntity object if present in {self._entities}, otherwise None
			Usage:
				self[entity]
				, where entity can either be:
					1. an str object
						In this case check {self._entities} keys.
						If not present in {self._entities}, use its formatted_entityname and check {self._helper_dicts['formatted_entitynames']} keys.
							Function format_text_fragment() is implemented in WikipediaEntity and used via TokenHandlerService
					2. an int object
						In this case check {self._helper_dicts['entity_ids']} keys.
					3. a WikipediaEntity object
						In this case use its text_fragment attribute and check {self._entities} keys.
		'''
		if isinstance(key, str):
			if key in self._entities:
				return self._get_redirected_entity(
					self._entities.get(key, None)
				)
			else:
				formatted_entityname = self._entity_handler.format_text_fragment(key)
				return self._get_redirected_entity(
					self._helper_dicts['formatted_entitynames'].get(formatted_entityname, None)
				)
		elif isinstance(key, int):
			return self._get_redirected_entity(
				self._helper_dicts['entity_ids'].get(key, None)
			)
		elif isinstance(key, self._entity_handler.token_type):
			return self._get_redirected_entity(
				self._entities.get(key.text_fragment, None)
			)

	def __setitem__(
		self,
		entityname: str,
		entity: WikipediaEntity
	) -> None:
		'''
			Assign WikipediaEntity object to {self._entities}.
			Usage:
				self[entityname] = entity
				, where entityname is an str object and entity is a WikipediaEntity object
		'''
		if isinstance(entity, self._entity_handler.token_type):
			self._entities[entityname] = entity

	def __contains__(
		self,
		key: object,
	) -> bool:
		'''
			Usage:
				entity in self
				, where entity can either be an str or a WikipediaEntity object
		'''
		if isinstance(key, self._entity_handler.token_type):
			key = key.text_fragment
		if isinstance(key, str):
			return key in self._entities
		return False

	def _get_disambig_entityids(self) -> list:
		'''
			File format: document id | document title
		'''
		disambig_pages = []
		src_file = 'wiki_disambiguation_pages.txt'
		path = self._datapath / src_file
		assert path.exists(), f'Invalid path {path}'
		with open(
			path,
			'r',
			encoding='utf-8',
		) as f:
			for line in f:
				try:
					disambig_pages.append(int(line[:line.index('\t')]))
				except:
					raise Exception(f'Invalid format: {src_file}')
		return disambig_pages

	def _set_redirects(
		self,
		excl_pages: list
	) -> None:
		'''
			File format: source unquoted URL | target unquoted URL | source document ID

			link example in document:
				<a 
					href="/wiki/%CE%94%CE%BF%CF%8D%CF%81%CE%B5%CE%B9%CE%BF%CF%82_%CE%8A%CF%80%CF%80%CE%BF%CF%82_(%CE%9B%CE%BF%CE%B3%CE%B9%CF%83%CE%BC%CE%B9%CE%BA%CF%8C)" 
					class="mw-redirect" 
					title="Δούρειος Ίππος (Λογισμικό)"
				>
					Δούρειος Ίππος
				</a>

			link example in wiki_redirects.txt:
				Δούρειος Ίππος (Λογισμικό)\tΔούρειος Ίππος (υπολογιστές)\t104817\n
		'''
		src_file = 'wiki_redirects.txt'
		path = self._datapath / src_file
		assert path.exists(), f'Invalid path {path}'
		with open(
			path, 
			'r',
			encoding='utf-8'
		) as f:
			for line in f:
				data = line.split('\t')
				try:
					source_document_title, target_document_title, source_document_id = (
						data[0], 
						data[1], 
						int(data[2]),
					)
				except:
					raise Exception(f'Invalid format: {src_file}')
				if target_document_title in self._entities and source_document_id not in excl_pages:
					if source_document_title not in self._entities:
						# add entity to {self._entities}
						token = self._entity_handler.build_token(source_document_title, source_document_id)
						self._entities[source_document_title] = token
						self._helper_dicts['formatted_entitynames'][token.formatted_entityname] = token
						self._helper_dicts['entity_ids'][token.entityid] = token
					source_token = self._entities[source_document_title]
					target_token = self._entities[target_document_title]
					source_token.redirect_to_entityid = target_token.entityid

	def build_entity_index(
		self, 
		exclude_disambiguation_pages: bool = True, 
		combine_redirects: bool = True
	) -> object:
		'''
			Desc:
				fill super()._entities dict w/ entity (doc ids and doc titles) Tokens
			File format:
				document title | document id
		'''
		print(f'Loading KB entities...')
		excl_pages = self._get_disambig_entityids() if exclude_disambiguation_pages else []
		src_file = 'wiki_name_id_map.txt'
		path = self._datapath / src_file
		assert path.exists(), f'Invalid path {path}'
		with open(path, 
			'r', 
			encoding='utf-8'
		) as f:
			for i, line in enumerate(f):
				data = line.split('\t')
				try:
					title, doc_id = (
						data[0], 
						int(data[1])
					)
				except:
					raise Exception(f'Invalid format: {src_file}')
				if doc_id not in excl_pages:
					token = self._entity_handler.build_token(title, doc_id)
					self._entities[title] = token
					self._helper_dicts['formatted_entitynames'][token.formatted_entityname] = token
					self._helper_dicts['entity_ids'][token.entityid] = token
		if combine_redirects:
			self._set_redirects(excl_pages)
		assert len(self._entities), 'No KB entities were loaded.'
		assert len(self._helper_dicts['entity_ids']) == len(self._entities), 'Entity ID - Entity Name is supposed to be a one-to-one relation.'
		print(
			f'Loaded KB entities successfully.'
			f'\n\tTotal KB entities: "{len(self._entities)}"')
		return self
