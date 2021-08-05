from EL.tokens.tokens.token_base import TokenBase

class TokenHandlerService():
	'''
		Dependency on a specified Token type via {self._token_type} for constructing such objects.
	'''
	
	def __init__(
		self,
		token_type: TokenBase,
	) -> object:
		assert issubclass(token_type, TokenBase), 'Invalid Token type.'
		self._token_type = token_type

	def format_text_fragment(
		self,
		text_fragment: str,
		token_type: type = None,
	) -> str:
		'''
			get token_type ( {self._token_type} by default ) 's format_text_fragment attribute.
			if such attribute exists and is callable:
				use it and return the result.
			else:
				return the input
		'''
		assert isinstance(text_fragment, str), 'Invalid input'
		token_type = token_type or self._token_type
		if (
			getattr(token_type, 'format_text_fragment', None) 
			and callable(token_type.format_text_fragment)
		):
			text_fragment = token_type.format_text_fragment(text_fragment) 
		return text_fragment

	@property
	def token_type(self) -> type:
		''' Returns class '''
		return self._token_type
		
	def set_token_type(
		self,
		token_type: type
	) -> object:
		assert issubclass(token_type, TokenBase), 'Invalid Token type.'
		self._token_type = token_type
		return self

	def build_token(
		self,
		*args,
		**kwargs,
	) -> object:
		return self._token_type(*args, **kwargs)