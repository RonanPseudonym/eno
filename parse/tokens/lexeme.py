from cli.ansi import *

class Base:
	def __init__(self, char, color, holds_data = False):
		self.char = char
		self.color = color

		self.position = None
		self.line_str = None

		self.holds_data = holds_data

		if holds_data: self.data = str()

		self.start = None
		self.line = None
		self.line_txt = None
		self.lbuffer = 0

	def __str__(self):
		if self.holds_data: return fstr('"'+self.data+'"', self.color)
		else: return fstr(self.char, self.color)

	def __len__(self):
		if self.holds_data: return len(self.data) + self.lbuffer
		if isinstance(self, Equality): return 2
		else: return 1

class TagOpening(Base):
	def __init__(self):
		Base.__init__(self, "<", YELLOW)

class TagClosing(Base):
	def __init__(self):
		Base.__init__(self, ">", YELLOW)

class Equality(Base):
	def __init__(self):
		Base.__init__(self, ":", RED)

class Negation(Base):
	def __init__(self):
		Base.__init__(self, "!", RED)

class NoClose(Base):
	def __init__(self):
		Base.__init__(self, "&", RED)

class TypeDef(Base):
	def __init__(self):
		Base.__init__(self, "+", RED)

class Fallback(Base):
	def __init__(self):
		Base.__init__(self, "=>", RED)


class Name(Base):
	def __init__(self):
		Base.__init__(self, str(), MAGENTA, holds_data = True)
	def __repr__(self): return self.data

class File(Base):
	def __init__(self):
		Base.__init__(self, str(), YELLOW, holds_data = True)
	def __repr__(self): return self.data

class String(Base):
	def __init__(self):
		Base.__init__(self, str(), GREEN, holds_data = True)
	def __repr__(self): return self.data

class Text(Base):
	def __init__(self):
		Base.__init__(self, str(), CYAN, holds_data = True)
	def __repr__(self): return self.data

class Input(Base):
	def __init__(self):
		Base.__init__(self, str(), BRED, holds_data = True)
	def __repr__(self): return self.data

class Output(Base):
	def __init__(self):
		Base.__init__(self, str(), BGREEN, holds_data = True)
	def __repr__(self): return self.data

class Snippet(Base):
	def __init__(self):
		Base.__init__(self, str(), WHITE, holds_data = True)
	def __repr__(self): return self.data


class Newline(Base):
	def __init__(self):
		Base.__init__(self, "\n", "")