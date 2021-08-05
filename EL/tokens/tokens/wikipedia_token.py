from EL.tokens.tokens.entity_token import BasicEntity
from EL.tokens.tokens.formatting.entity_formatting_en import EntityFormattingEN
from EL.tokens.tokens.formatting.entity_formatting_el import EntityFormattingEL
from EL.config import config_settings

class WikipediaEntity(BasicEntity):
	'''
		A WikipediaEntity is a document present in the wiki dump
	'''

	_lang = config_settings.get('language', None)

	def __init__(
		self,
		document_title: str,
		document_id: int,
		redirect_to_document_id: int = None,
	):
		super().__init__(document_title, document_id)
		self._formatted_entityname = self.format_text_fragment(document_title)
		self._entityid = document_id
		self._redirect_to_entityid = redirect_to_document_id

	@classmethod
	def format_text_fragment(
		cls,
		text_fragment: str,
	) -> str:
		'''
			Return simplified version of {text_fragment}.
		'''
		if cls._lang:
			if cls._lang == 'en':
				return EntityFormattingEN.apply_rules(text_fragment)
			elif cls._lang == 'el':
				return EntityFormattingEL.apply_rules(text_fragment)
		return text_fragment

	@property
	def formatted_entityname(self) -> str:
		return self._formatted_entityname
	
	@formatted_entityname.setter
	def formatted_entityname(self, formatted_entityname: str) -> None:
		# preprocessing must have occured
		self._formatted_entityname = formatted_entityname
	
	@formatted_entityname.deleter
	def formatted_entityname(self) -> None:
		self._formatted_entityname = ''

	@property
	def redirect_to_entityid(self) -> int:
		return self._redirect_to_entityid

	@redirect_to_entityid.setter
	def redirect_to_entityid(self, redirect_to_document_id: int) -> None:
		if isinstance(redirect_to_document_id, int):
			self._redirect_to_entityid = redirect_to_document_id
	
	@redirect_to_entityid.deleter
	def redirect_to_entityid(self) -> None:
		self._redirect_to_entityid = None

	def __hash__(self) -> hash:
		return hash(('wikipedia', self._text_fragment, self._entityid))

	def __repr__(self) -> str:
		return (
			f'{super().__repr__()},\n'
			f'\tText (simplified): {self._formatted_entityname},\n'
			f'\tRedirect to Entity ID: {self._redirect_to_entityid}'
		)
