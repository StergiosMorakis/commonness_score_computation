import unicodedata
from nltk.corpus import stopwords
# import re

########
########
######
####
##		Functions for Greek
####
######
########
########

def remove_diactitical_marks(
	text_fragment: str,
	diactitical_marks: str = "´΄’'\""
	) -> str:
	for diactitical_mark in diactitical_marks:
		text_fragment = text_fragment.replace(diactitical_mark, '')
	return text_fragment

def firstletter_greeklish_to_greek(text_fragment: str):
	'''
		/ Custom approach /
		Issue to solve: 
			Greek letters (once capitalized) can be easily mistaken for english ones.
			For example, the capital greek letter Α looks the same as the english capital letter A, although α != a if lowercased.
			This leads to mismatches, i.e. 'mεγάλος' != 'μεγάλος' (although 'Mεγάλος' does look the same as 'Μεγάλος').
			In the greek wikipedia, authors did have some happy accidents I aim to fix.
		Note:
			Greeklish is writing in greek using english chars. This function is not meant for that.
			It is merely used for 'adjusting' minor author typos in wikipedia urls.
		Function description:
			Input:
				lowercased str text
			if text:
				1. has an english letter as its first one,
				2. no other letters are english and
				3. has at least one greek letter
			then:
				transform the first letter to the respective greek one
	'''
	greek_alphabet = (
		'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ' , 'φ', 'χ', 'ψ', 'ω'
	)
	greeklish_mapping = {
		'a': greek_alphabet[0],		# α
		'b': greek_alphabet[1],		# β
		'e': greek_alphabet[4],		# ε
		'h': greek_alphabet[6],		# η
		'i': greek_alphabet[8],		# ι
		'k': greek_alphabet[9],		# κ
		'm': greek_alphabet[11],	# μ
		'n': greek_alphabet[12],	# ν
		'o': greek_alphabet[14],	# ο
		'p': greek_alphabet[16],	# ρ
		'q': greek_alphabet[13],	# ο
		'r': greek_alphabet[16],	# ρ (?)
		's': greek_alphabet[17],	# σ
		't': greek_alphabet[18],	# τ
		'u': greek_alphabet[19],	# υ (?)
		'v': greek_alphabet[12],	# υ (?)
		'w': greek_alphabet[23],	# ω
		'x': greek_alphabet[21],	# χ
		'y': greek_alphabet[19],	# υ
		'z': greek_alphabet[5],		# ζ
	}
	if (
		text_fragment.islower() 	# False if empty
		and text_fragment[0] in greeklish_mapping 
		and sum([ch in greeklish_mapping for ch in text_fragment]) == 1
		and sum([ch in greek_alphabet for ch in text_fragment]) > 0
	):
		return greeklish_mapping[text_fragment[0]] + text_fragment[1:]
	return text_fragment

def translate_letter(c: chr, source_lang: str = None, target_lang: str = None) -> chr:
	'''
		*** Not used ***
		( & never should. )
	'''
	engish_to_greek = {
		'A': 'Α', 'B': 'Β', 'C': 'Γ', 'D': 'Δ', 'E': 'Ε', 'F': 'Φ', 'G': 'Φ', 'H': 'Η', 'I': 'Ι', 'J': 'Ξ', 'K': 'Κ', 'L': 'Λ', 'M': 'Μ', 'N': 'Ν', 'O': 'Ο', 'P': 'Ρ', 'Q': 'Ξ', 'R': 'Ρ', 'S': 'Σ', 'T': 'Τ', 'U': 'Υ', 'V': 'Ν', 'W': 'Ω', 'X': 'Χ', 'Y': 'Υ', 'Z': 'Ζ',
	}
	greek_to_english = {
		'Α': 'A', 'Β': 'B', 'Γ': 'G', 'Δ': 'D', 'Ε': 'E', 'Ζ': 'Z', 'Η': 'H', 'Θ': 'U', 'Ι': 'I', 'Κ': 'K', 'Λ': 'L', 'Μ': 'M', 'Ν': 'N', 'Ξ': 'J', 'Ο': 'O', 'Π': 'P', 'Ρ': 'P', 'Σ': 'S', 'Τ': 'T', 'Υ': 'Y', 'Φ': 'F', 'Χ': 'X', 'Ψ': 'C', 'Ω': 'V',
	}
	if source_lang == 'english':
		if target_lang == 'greek':
			return engish_to_greek.get(c, c)
	if source_lang == 'greek':
		if target_lang == 'greek':
			return engish_to_greek.get(c, c)
	return c

def strip_accents(text_fragment: str) -> str:
	'''
		Example: 
			strip_accents('Γαϊδούρι του φωτός.') => 'Γαιδουρι του φωτος.'
		Should work for french too.
	'''
	return ''.join(
		[
			c
			for c
			in unicodedata.normalize('NFKD', text_fragment)
			if not unicodedata.combining(c)
		]
	)

########
########
######
####
##		Multilingual Functions
####
######
########
########


def get_nltk_stopwords(lang = '') -> set:
	'''
		if lang = 'greek':
			example stopwords sample  == [
				'αλλα', 'αν', 'αντι', ..., 'οὖν', 'οὗ', 'οὗτος', 'οὗτοσ', ..., 'ἡ', 'ἢ', 'ἣ', 'ἤ', 'ἥ', ..., 
			]
		Note:
			Roughly half of the Greek stopwords are invalid for Modern Greek. 
			Most accents used and some of the words are Ancient Greek.
	'''

	def get_lang(lang: str) -> str:
		langs = {
			'el': 'greek',
			'en': 'english',
		}
		return langs.get(lang, '')

	lang = get_lang(lang)
	if lang:
		return {strip_accents(word.lower()) for word in stopwords.words(lang)}
	return set()

def is_stopword(word: str, lang: str = '') -> bool:
	return strip_accents(word.lower()) in get_nltk_stopwords(lang)

def is_important_word(word: str, lang: str = '') -> bool:
	'''
		words has length > 1 & is not numeric & is not stopword
	'''
	return len(word) > 1 and not word.isnumeric() and not is_stopword(word, lang)
	
if __name__ == '__main__':
	test_case = 'Ένα γαϊδούρι 0,'
	print(
		'Testing: "',
		test_case,
		'", Result: "',
		remove_greek_accents(test_case),
		'".'
	)
