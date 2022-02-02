from parse.tokens.lexeme import *
from parse.tokens.tagger import *
import cli

class Tagger:
	def __init__(self, filename, lexemes):
		self.filename = filename
		self.lexemes = lexemes
		self.tagsoup = []
		self.open = None
		self.pos = 0

	def l(self):
		return len(self.lexemes)

	def advance(self):
		self.pos += 1

		if self.pos >= self.l(): 
			return None
		return self.lexemes[self.pos]

	def err(self, name, **kwargs):
		cli.err(name, self.filename, (self.current().start, self.current().start + (len(self.current()) - 1)), self.current().line, self.current().line_txt, **kwargs)

	def previous(self):
		if self.pos - 1 < 0: 
			return None
		return self.lexemes[self.pos - 1]

	def peek(self, look = 1):
		if self.pos + look >= self.l(): 
			return None
		return self.lexemes[self.pos + look]

	def current(self):
		return self.lexemes[self.pos]

	def nameplus(self):
		if isinstance(self.peek(), Equality):
			self.open.settings[self.current()] = self.peek(look = 2)
			key = self.current()

			self.advance()
			self.advance()

			if isinstance(self.peek(), Fallback):
				total_fallback = CascadingFallback()
				while True:
					total_fallback.append(self.current())

					if not isinstance(self.peek(), Fallback):
						break

					self.advance()
					self.advance()

				self.open.settings[key] = total_fallback
		else:
			if isinstance(self.current(), Name):
				if not self.open.name:
					self.open.name = self.current()
				else:
					self.err("MultipleNamesInvalid")
			else:
				self.err("EventNotValidName")

	def walk(self):
		lexeme = self.current()

		match type(lexeme).__name__:
			case "TagOpening":
				self.open = NHTag()

				self.open.start    = lexeme.start
				self.open.line     = lexeme.line
				self.open.line_txt = lexeme.line_txt

			case "TagClosing":
				if not self.open.name:
					self.err("TagEmpty")

				self.open.end = self.current().start + len(self.current())

				self.tagsoup.append(self.open)
				self.open = None

			case "Negation":
				if self.open.closing_tag: self.err("TagAlreadyMarked", char = "!")
				self.open.closing_tag = True
				if not self.open.can_close: self.err("ClosingDemitag")
				if self.open.is_typedef: self.err("ClosingTypedef")
				if self.open.name: self.err("CharacterOrder", char = "!")

			case "NoClose":
				if not self.open.can_close: self.err("TagAlreadyMarked", char = "&")
				self.open.can_close = False
				if self.open.closing_tag: self.err("ClosingDemitag")
				if self.open.name: self.err("CharacterOrder", char = "&")

			case "TypeDef":
				if self.open.is_typedef: self.err("TagAlreadyMarked", char = "+")
				self.open.is_typedef = True
				if self.open.closing_tag: self.err("ClosingTypedef")
				if self.open.name: self.err("CharacterOrder", char = "+")

			case "Text":
				self.tagsoup.append(self.current())

			case "Name":
				self.nameplus()

			case "Input":
				self.nameplus()

		if self.advance() != None:
			self.walk()
		else:
			cli.ok("Tagged "+self.filename)

	def pretty_print(self):
		print("".join([str(i) for i in self.tagsoup]))