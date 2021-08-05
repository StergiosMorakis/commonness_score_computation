from EL.tokens.tokens.token_base import TokenBase

class BasicEntity(TokenBase):
	'''
		Base class for Entities
		Subclass of TokenBase
	'''

	def __init__(
		self,
		entityname: str,
		entityid: int,
	) -> object:
		assert entityid >= 0, 'Invalid Entity ID'
		super().__init__(entityname)
		self._entityid = entityid

	def __hash__(self) -> hash:
		'''
			Entity objects are used as dictionary keys (for p(e|m) computation) and must therefore provide a hash key.
			Based on Python 3.6 documention a hash function is most efficient when used on a tuple.
		'''
		return hash((self._text_fragment, self._entityid))

	@property
	def entityid(self) -> int:
		return self._entityid

	@entityid.setter
	def entityid(self, entityid: int) -> None:
		if isinstance(entityid, int) and entityid >= 0:
			self._entityid = entityid

	@entityid.deleter
	def entityid(self) -> None:
		self._entityid = None

	def __eq__(self, other: object) -> bool:
		'''
			BasicEntity objects are now comparable to:
				str,
				int,
				objects with type that is a subclass of BasicEntity 
		'''
		if isinstance(other, str):
			return self._text_fragment == other
		elif isinstance(other, int):
			return self._entityid == other
		elif isubclass(type(other), BasicEntity):
			return (self._text_fragment, self._entityid) == (other._text_fragment, other._entityid)
		return False

	def __repr__(self) -> str:
		return (
			f'{super().__repr__()},\n'
			f'\tEntity ID: {self._entityid}'
		)
