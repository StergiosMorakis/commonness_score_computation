from EL.utils.helper_funcs import strip_accents, firstletter_greeklish_to_greek, remove_diactitical_marks
from EL.tokens.tokens.formatting.entity_formatting_base import EntityFormattingBase

class EntityFormattingEL(EntityFormattingBase):
	_stacked_formatting_funcs = [
			strip_accents,
			remove_diactitical_marks,
			firstletter_greeklish_to_greek,
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

