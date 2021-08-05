from EL.tokens.token_handler_service import TokenHandlerService
from EL.tokens.tokens.mention_token import MentionToken
from EL.pem_indexers.pem_controller import PemController
import abc

class PemIndexerBase(metaclass=abc.ABCMeta):
	'''
		Class responsible for computing P( entity | mention )
		Note:
			Implement Subclass for usage.
			Subclasses must implement the build_pem_index() function.
			Function build_pem_index() is responsible for counting entities per mention.
	'''
	def __init__(
		self, 
		datapath: object,
	):
		self._datapath = datapath 									# Path object
		self._pem_controller = PemController.get_instance()			# many( PemIndexers )-to-one( PemController ) relation
		self._mention_builder = TokenHandlerService(MentionToken)	# Used for constructing MentionToken objects
		self._mentions: dict = {}									# text_fragment as key, MentionToken as value

	@abc.abstractmethod	
	def build_pem_index(
		self
	) -> None:
		pass
		
	@property
	def datapath(self) -> object:
		return self._datapath

	@property
	def mentions(self):
		return self._mentions
	
	def __getitem__(
		self,
		mention: object,
	) -> MentionToken:
		'''
			Return either self._mentions[mention] value or None if not present in {self._mentions}
			Usage:
				self[mention]
				, where mention can either be an str object or a MentionToken object
		'''
		if isinstance(mention, MentionToken):
			mention = mention.text_fragment
		if isinstance(mention, str):
			return self._mentions.get(mention, None)

	def __setitem__(
		self,
		mention: object,
		updated_mention: MentionToken,
	) -> None:
		'''
			Assign MentionToken object to {self._mentions}.
			Usage:
				self[mention] = new_mention
				, where mention is either an str object or a MentionToken object and new_mention is a MentionToken object
		'''
		if isinstance(mention, MentionToken):
			mention = mention.text_fragment
		if isinstance(mention, str) and isinstance(updated_mention, MentionToken):
			self._mentions[mention] = updated_mention

	def __delitem__(
		self,
		mention: object,
	) -> None:
		'''
			Usage: 
				del self[mention]
				, where mention can either be an str object or a MentionToken object
		'''
		if isinstance(mention, MentionToken):
			mention = mention.text_fragment
		if isinstance(mention, str):
			del self._mentions[mention]

	def __len__(self) -> int:
		return len(self._mentions)

	def __iter__(self) -> iter:
		for mention in self._mentions:
			yield self._mentions[mention]

	def __contains__(
		self,
		mention: object,
	) -> bool:
		'''
			Usage: 
				mention in self
				, where mention can either be an str object or a MentionToken object
		'''
		if isinstance(mention, MentionToken):
			mention = mention.text_fragment
		if isinstance(mention, str):
			return mention in self._mentions
		return False
