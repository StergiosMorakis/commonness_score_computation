from EL.tokens.tokens.token_base import TokenBase
from EL.tokens.tokens.entity_token import BasicEntity

class MentionToken(TokenBase):
	'''
		MentionToken is used for P(e|m) computation.
		Stores entities assigned to itself as keys and their corresponding counts as values.
		Such entity objects must be subclasses of the BasicEntity class.
	'''

	def __init__(
		self,
		text_fragment: str,
	) -> object:
		super().__init__(text_fragment)
		self._entities: dict = {}
		self._occurences: int = 0

	@property
	def occurences(self) -> int:
		if self._occurences > 0:
			return self._occurences
		return self._get_entity_values_sum()
		
	
	def _entity_reduction(
		self,
		max_items: int = None,
	) -> dict:
		'''
			Desc:
				1. order {self._entities} dictionary by value and create list [(BasicEntity_A, int_A), (BasicEntity_B, int_B) ...]
				2. keep top {max_items} entities
				3. turn list of tuples into a dictionary
				4. return the generated dictionary
		'''
		return {
			entity: count
			for entity, count
			in sorted(
				self._entities.items(),
				reverse = True,
				key=lambda item: item[1]
			)[:max_items]	# unfiltered if {max_items} is None else filtered
		}

	def _get_entity_values_sum(self) -> int:
		'''
			Desc:
				Return sum of {self._entities} values (occurences).
		'''
		return sum(self._entities.values())

	def items(self) -> iter:
		'''
			Desc:
				yield tuple(entity, count)
				, where entity is a subclass of the BasicEntity class and count is int or float.
		'''
		for entity, count in self._entities.items():
			yield entity, count

	def compute_pem(
		self,
		entity_limit: int = None
	) -> None:
		if not self._occurences:
			self._entities = self._entity_reduction(entity_limit)					# reduce entities
			self._occurences = self._get_entity_values_sum()						# get total sum of reduced entity counts and update {self._occurences}
			for entity in self._entities:
				self._entities[entity] = self._entities[entity] / self._occurences	# change {self._entities} values to the computed p(e|m) value

	@property
	def entities(self) -> dict:
		return self._entities
	
	@entities.deleter
	def entities(self) -> None:
		del self._entities

	def add_entities(
		self,
		other: object
	) -> object:
		'''
			Desc:
				Function used for updating Entity counts
			input:
				other is either another MentionToken object or any object that is a subclass of the BasicEntity class.
				* duck-typed for lists, tuples and sets of such (as long as they are all of the same type).
				if input is:
					1. MentionToken object:
						combine them and update self
					2. BasicEntity subclass object:
						initialise if that entity does not exist in {self._entities} and update count
		'''
		###
		# Duck Typing
		if (
			isinstance(other, list)
			or isinstance(other, tuple)
			or isinstance(other, set)
		):
			other = list(other)
		elif (
			isinstance(other, MentionToken)
			or issubclass(type(other), BasicEntity)
		):
			other = [other]
		else:
			raise NotImplementedError
		###
		if (
			all(isinstance(element, type(other[0])) for element in other[1:])
			and (
				isinstance(other[0], MentionToken)
				or issubclass(type(other[0]), BasicEntity)
			)
		):
			for element in other:
				if isinstance(element, MentionToken):
					for entity in element:
						if entity not in self._entities:
							self[entity] = 0
						self._entities[entity] = self._entities[entity] + element[entity]
				elif issubclass(type(element), BasicEntity):
					if element not in self._entities:
						self[element] = 0
					self[element] += 1
		return self

	def __getitem__(
		self,
		entity: object
	) -> float:
		'''
			Desc:
				Return the entity value assigned to this mention, otherwise 0.
			Usage:
				self[entity]
				, where entity is a subclass of the BasicEntity class.
		'''
		return self._entities.get(entity, 0)

	def __setitem__(
		self,
		entity: object,
		value: float,
	) -> None:
		'''
			Desc:
				Assign a new value to specified entity for this mention.
			Usage:
				self[entity] = 0.64
				, where entity is a subclass of the BasicEntity class.
		'''
		if issubclass(type(entity), BasicEntity):
			self._entities[entity] = value

	def __delitem__(
		self,
		entity: object,
	) -> None:
		'''
			Usage: 
				del self[entity]
				, where entity is a subclass of the BasicEntity class.
		'''
		if issubclass(type(entity), BasicEntity):
			del self[entity]

	def __len__(self) -> int:
		'''
			Desc:
				get total distinct entities
			Usage: 
				len(self)
		'''
		return len(self._entities)

	def __iter__(self) -> iter:
		'''
			Usage: 
				for entity in self:
					...
				, where entity is a subclass of the BasicEntity class.
		'''
		for entity in self._entities:
			yield entity

	def __contains__(
		self,
		entity: object,
	) -> bool:
		'''
			Usage: 
				entity in self
				, where entity is a subclass of the BasicEntity class.
		'''
		return entity in self._entities

	def __repr__(self) -> str:
		return (
			f'{super().__repr__()},\n'
			f'\tDistinct entities assigned: {len(self._entities)}'
		)