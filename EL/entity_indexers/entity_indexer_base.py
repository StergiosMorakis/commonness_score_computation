from EL.tokens.token_handler_service import TokenHandlerService
from EL.tokens.tokens.wikipedia_token import BasicEntity
import abc

class EntityIndexerBase(metaclass=abc.ABCMeta):
	'''
		Class responsible for loading entities from a Knowledge Base (KB).
		Note:
			Implement Subclass for usage.
			Subclass must implement the build_entity_index() function.
			Function build_entity_index() is responsible for filling the {self._entities} dictionary with entities in the KB.
	'''

	def __init__(
		self, 
		datapath: object,
	):
		self._entity_handler = TokenHandlerService(BasicEntity) 		# Used for constructing BasicEntity objects
		self._datapath = datapath										# Path object
		self._entities: dict = {}		 								# Entity Name as key, ID as value

	@abc.abstractmethod
	def build_entity_index(
		self
	) -> None:
		''' 
			Must be implemented in subclass 
			and executed by the user for creating the KB index.
		'''
		pass

	def items(self) -> iter:
		'''
			Similar to dict.items() generator
			yield tuple(str, BasicEntity)
		'''
		for entityname in iter(self):
			yield entityname, self._entities[entityname],

	@property
	def datapath(self) -> object:
		return self._datapath

	def __getitem__(
		self,
		entity: object,
	) -> object:
		'''
			Return either self._entities[entity] value or None if not present in self._entities
			Usage:
				self[entity]
				, where entity can either be an str object or any subclass of TokenBase
					(BasicEntity is subclass of TokenBase)
		'''
		if isubclass(type(entity), BasicEntity.__bases__[0]):
			entity = entity.text_fragment
		return self._entities.get(entity, None)

	def __setitem__(
		self,
		entityname: str,
		entityid: int,
	) -> None:
		'''
			Assign BasicEntity object to {self._entities}.
			entityname in REL is a unique field and can therefore be used as key.
			Usage:
				self[entityname] = entityid
				, where entityname is an str object and entityid is an int object
		'''
		self._entities[entityname] = self._entity_handler.build_token(entityname, entityid)

	def __delitem__(
		self,
		entity: object,
	) -> None:
		'''
			Usage: 
				del self[entity]
				, where entity can either be an str object or any subclass of TokenBase
					(BasicEntity is subclass of TokenBase)
		'''
		if isubclass(type(entity), BasicEntity.__bases__[0]):
			entity = entity.text_fragment
		del self._entities[entity]

	def __len__(self) -> int:
		'''
			Usage: 
				len(self)
		'''
		return len(self._entities)

	def __iter__(self) -> iter:
		'''
			Usage: 
				for entityname in self:
					...
		'''
		for entityname in self._entities:
			yield entityname

	def __contains__(
		self,
		entity: object,
	) -> bool:
		'''
			Usage: 
				entity in self
				, where entity can either be an str object or any subclass of TokenBase
					(BasicEntity is subclass of TokenBase)
		'''
		if isubclass(type(entity), BasicEntity.__bases__[0]):
			entity = entity.text_fragment
		return entity in self._entities
