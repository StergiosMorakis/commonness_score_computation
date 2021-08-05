from EL.tokens.tokens.formatting.entity_formatting_base import EntityFormattingBase

class EntityFormattingEN(EntityFormattingBase):
	_stacked_formatting_funcs = [
	]

	@classmethod
	def apply_rules(
		cls,
		text_fragment: str,
	) -> str:		
		text_fragment = super().apply_rules(text_fragment)
		for formatting_func in cls._stacked_formatting_funcs:
			text_fragment = formatting_func(text_fragment)
		return text_fragment
