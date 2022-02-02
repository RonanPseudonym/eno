from cli.ansi import *
from collections.abc import Sequence

class CascadingFallback(Sequence):
	def __init__(self):
		super().__init__()
		self.elements = []
	def __getitem__(self, i):
		return self.elements[i]
	def __len__(self):
		return len(self.elements)
	def append(self, i):
		self.elements.append(i)
	def __repr__(self):
		return fstr(" => ", YELLOW).join(list(map(str, self.elements)))

class NHTag:
	def __init__(self):
		self.name = None
		self.settings = {}

		self.can_close = True
		self.closing_tag = False
		self.is_typedef = False
		self.stage = 0

		self.start = 0
		self.end = 0

	def __repr__(self):
		components = []

		if self.closing_tag: components.append(fstr("!", YELLOW))
		if self.is_typedef: components.append(fstr("+", YELLOW))
		if not self.can_close: components.append(fstr("&", YELLOW))

		if self.name: components.append(self.name)

		for i in self.settings:
			components.append(" "+str(i)+fstr(":", YELLOW)+str(self.settings[i]))

		return fstr("<", YELLOW) + "".join(map(str, components)) + fstr(">", YELLOW)