class PemController():
	_instance = None

	@staticmethod 
	def get_instance():
		assert PemController._instance, 'Calling Null instance'
		return PemController._instance

	def __init__(
		self,
		entity_indexer: object,
		datapath: object
	):
		assert not PemController._instance, \
			f'Not allowing multiple instances of {self.__class__.__name__}'
		self._entity_indexer = entity_indexer
		self._datapath = datapath
		self._pem_indexers  = []
		self._mention_counts = {}
		self._pem = {}
		PemController._instance = self

	@property	
	def entity_indexer(
		self
	) -> object:
		return self._entity_indexer

	@property
	def datapath(self) -> object:
		return self._datapath

	def attach(
		self,
		pem_indexers: object,
	) -> object:
		''' 
			Desc:
				Attach pem_indexer objects (Sub-classes of PemIndexerBase) for computing the p(e|m) index.
				Input can either be a single subclass object of PemIndexerBase or an iterable object of them.
		'''
		###
		# Duct-taping
		if pem_indexers.__class__.__bases__[0].__name__ == 'PemIndexerBase':
			pem_indexers = [pem_indexers]
		elif (
			isinstance(pem_indexers, list)
			or isinstance(pem_indexers, tuple)
			or isinstance(pem_indexers, set)

		):
			pem_indexers = list(pem_indexers)
		else:
			raise NotImplementedError
		###
		assert all(pem_indexer.__class__.__bases__[0].__name__ == 'PemIndexerBase' for pem_indexer in pem_indexers), 'Unexpected input - cannot attach'
		for pem_indexer in pem_indexers:
			self._pem_indexers.append(pem_indexer)
		return self

	def build_pem_index(self) -> object:
		'''
			Desc:
				Run the build_pem_index() function of each pem_indexer attached to this object.
		'''
		assert len(self._pem_indexers), 'No PemIndexer objects have been attached. Use .attach() method.'
		for pem_indexer in self._pem_indexers:
			pem_indexer.build_pem_index()
		# round p(e|m) value to 3 decimals
		for mention in self._pem:
			for entity in self._pem[mention]:
				self._pem[mention][entity] = round(
					self._pem[mention][entity],
					3
				)
		print(
			'P(e|m) index computed successfully.\n'
			f'\tTotal distinct mentions: "{len(self._pem)}"'
		)
		return self

	def update_pem(
		self,
		pem_indexer: object
	) -> None:
		'''
			Desc:
				Called externally, after a pem_indexer's successful build_pem_index() computation - on the pem_indexer's end.
				Once all mention objects have retrieved their entities per pem_indexer, MentionToken.compute_pem() is called on each of them.
		'''
		assert pem_indexer.__class__.__bases__[0].__name__ == 'PemIndexerBase', 'Unexpected object as input - must be SubClass of PemIndexerBase'
		if len(pem_indexer):
			entities_per_mention_limit: int = 100
			for mention in pem_indexer:
				mention.compute_pem(entities_per_mention_limit)
				if str(mention) not in self._pem:
					self._mention_counts[str(mention)] = mention.occurences
					self._pem[str(mention)] = {
						str(entity): pem
						for entity, pem in mention.items()
					}
				else:
					# condition branch in case of len(self._pem_indexers) > 1
					self._mention_counts[str(mention)] += mention.occurences
					for entity, pem in mention.items():
						if str(entity) in self._pem[str(mention)]:
							self._pem[str(mention)][str(entity)] = min(
								len(self._pem_indexers) / 2, # Ad-hoc approach for setting upper-bound
								self._pem[str(mention)][str(entity)] + pem
							)
						else:
							self._pem[str(mention)][str(entity)] = pem
			print(f'P(e|m) values have been computed successfully.')

	def reset_state(
		self
	) -> object:
		self._pem_indexers  = []
		self._mention_counts = {}
		self._pem = {}
		return self

	def store(self) -> object:
		'''
			Desc:
				Store {self._pem} and {self._mention_counts} in db
		'''
		path = self._datapath / 'generated'
		path.mkdir(exist_ok = True)
		##
		# (To-be-filled) code block for storing 
		# self._pem and self._mention_counts in local db

		##
		return self