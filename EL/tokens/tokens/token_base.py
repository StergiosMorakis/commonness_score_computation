class TokenBase():
	'''
		Base class for Tokens
	'''

	def __init__(
		self,
		text_fragment: str
	):
		self._text_fragment = text_fragment

	@property
	def text_fragment(self) -> str:
		return self._text_fragment

	@text_fragment.setter
	def text_fragment(
		self,
		text_fragment: str
	) -> None:
		if isinstance(text_fragment, str) and text_fragment:
			self._text_fragment = text_fragment
			
	@text_fragment.deleter
	def text_fragment(
		self
	) -> None:
		self._text_fragment = ''

	def __eq__(self, other: object) -> bool:
		if isinstance(other, str):
			return self.text_fragment == other
		elif isinstance(other, TokenBase):
			return self.text_fragment == other.text_fragment
		return False

	def __repr__(self) -> str:
		return (
			f'<{self.__class__.__name__}>\n'
			f'\tText: {self._text_fragment}'
		)

	def __str__(self) -> str:
		return self._text_fragment