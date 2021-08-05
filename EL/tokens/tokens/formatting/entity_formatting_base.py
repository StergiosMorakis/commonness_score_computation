from EL.tokens.tokens.formatting.formatting_base import FormattingBase

class EntityFormattingBase(FormattingBase):

	@classmethod
	def apply_rules(
		cls,
		text_fragment: str,
	) -> str:		
		text_fragment = ' '.join(
			text_fragment 				\
			.replace('&amp;', r'&')		\
			.replace('&quot;', r'"')	\
			.replace('&#039;', r"'")	\
			.replace('_', r" ")			\
			.split()
		).lower()
		return text_fragment