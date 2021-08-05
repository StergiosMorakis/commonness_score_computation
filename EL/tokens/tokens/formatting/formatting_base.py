import abc

class FormattingBase(metaclass=abc.ABCMeta):

	@classmethod
	@abc.abstractmethod
	def apply_rules(
		cls,
		text_fragment: str,
	) -> str:
		pass
