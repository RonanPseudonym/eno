import parse.tokens as token
import cli

class Lexer:
	def __init__(self, filename):
		self.filename = filename

		cli.ok("Initializing "+self.filename)

		self.text = f = open(filename, 'r').read()

		cli.ok("Read "+self.filename)

		self.pos = 0

		self.lexemes = []
		self.in_tag = False

		self.open = None

	def l(self):
		return len(self.text)

	def cpos(self):
		count = 0
		lcount = 0

		data = {}

		for i in self.text.split("\n"):
			count += len(i) + 1
			lcount += 1

			if self.pos < count:
				data["index"] = self.pos - (count - len(i)) + 1
				data["lnum"] = lcount
				data["text"] = i

				return data

	def advance(self):
		self.pos += 1

		if self.pos >= self.l(): 
			return None
		return self.text[self.pos]

	def err(self, name):
		pos = self.cpos()
		cli.err(name, self.filename, (pos["index"], pos["index"]), pos["lnum"], pos["text"])

	def previous(self):
		if self.pos - 1 < 0: 
			return None
		return self.text[self.pos - 1]

	def peek(self):
		if self.pos + 1 >= self.l(): 
			return None
		return self.text[self.pos + 1]

	def current(self):
		return self.text[self.pos]

	def add_lex(self, _type):
		self.lexemes.append(_type())
		self.lexeme_add_metadata()

	def close_text(self):
		if self.open: 
			self.lexemes.append(self.open)
			self.lexeme_add_metadata()
			self.open.start -= len(self.open)

			if not isinstance(self.open, token.Text):
				self.open.start -= 1
				self.open.lbuffer = 1

			self.open = None

	def lexeme_add_metadata(self):
		data = self.cpos()

		self.lexemes[-1].start = data["index"]
		self.lexemes[-1].line = data["lnum"]
		self.lexemes[-1].line_txt = data["text"]

	def walk(self):
		if self.in_tag:
			if isinstance(self.open, token.Snippet):
				if self.current() == "]":
					self.close_text()
				else:
					self.open.data += self.current()

			else:
				match self.current():
					case ">":
						self.close_text()
						self.add_lex(token.TagClosing)

						self.in_tag = False

					case "<":
						self.err("OpeningMultipleTags")

					case ":":
						self.close_text()

						self.add_lex(token.Equality)

					case "!":
						self.add_lex(token.Negation)

					case "&":
						self.add_lex(token.NoClose)

					case "+":
						self.add_lex(token.TypeDef)

					case "=":
						self.close_text()

						if self.peek() == ">":
							self.add_lex(token.Fallback)
							self.advance()
						else:
							self.err("EqualsNotValidCharacter")

					case "#":
						self.open = token.String()

					case "*":
						self.open = token.File()

					case "@":
						self.open = token.Input()

					case "$":
						self.open = token.Output()

					case " ":
						self.close_text()

					case "\n":
						self.close_text()

					case "\t":
						self.close_text()

					case "[":
						self.open = token.Snippet()

					# case "(":
					# 	self.add_lex(token.LeftBracket)

					# case ")":
					# 	self.close_text()
					# 	self.add_lex(token.RightBracket)

					case _:
						if isinstance(self.open, token.Snippet):
							self.open.data += self.current()
						elif self.current().isalnum() or self.current() == "_":
							if self.open == None:
								self.open = token.Name()

							self.open.data += self.current()
						else:
							self.err("ForeignCharInTag")

		else:
			if self.current != ">":
				match self.current():
					case "<":
						if self.previous() != "\\":
							self.close_text()
							self.add_lex(token.TagOpening)
							self.in_tag = True
						else:
							if self.open:
								self.open.data += "<"
					case _:
						if self.current() != "\t":
							if self.open:
								if not (self.current() == "\\" and self.peek() == "<"):
									self.open.data += self.current()
							elif self.current() != "\n":
								# print(self.c)
								self.open = token.Text()
								if (not len(self.open.data) or self.open.data[-1] != "\n"): self.open.data += self.current()

		if self.advance() != None:
			self.walk()
		else:
			cli.ok("Tokenized "+self.filename)

	def pretty_print(self):
		for i in self.lexemes:
			print(i, end="")