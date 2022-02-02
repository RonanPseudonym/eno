from collections.abc     import Sequence
from parse.tokens.tagger import NHTag
from enum                import Enum

import cli.ansi as ansi

class ValueTypes(Enum):
	NAME    = 0
	STRING  = 1

	FILE    = 100

	INPUT   = 200

	OUTPUT  = 300
	SNIPPET = 301

class Demitag:
	def __init__(self, *args):
		self._name = None
		self._typedef = False
		self._types = {}

		if args:
			self._name = args[0]

	def add_attr(self, name, value):
		setattr(self, name, value)

	def __str__(self):
		name = ansi.fstr("+ ", ansi.RED) if self._typedef else ""
		name += ansi.fstr("&"+self._name, ansi.YELLOW)

		for (i, j) in vars(self).items():
			if not i.startswith("_"): name += " " + ansi.fstr(i, ansi.MAGENTA) + ansi.fstr(" : ", ansi.YELLOW) + ansi.fstr(j, ansi.MAGENTA)

		return name

	def set_type(self, key, t):
		if isinstance(t, str): 
			t = getattr(ValueTypes, t)

		self._types[key] = t

class Tag(Sequence):
	def __init__(self, *args):
		super().__init__()

		self._children = []
		self._name = None
		self._typedef = False
		self._types = {}

		self._open = True

		if args:
			self._name = args[0]

	def __getitem__(self, i):
		if isinstance(i, int):
			return self._children[i]
		elif isinstance(i, str):
			for j in self._children:
				if isinstance(j, Tag):
					if j.name == i:
						return j

	def __matmul__(self, anchor_str):
		return self._walk(self, "anchor", anchor_str)

	def _walk(self, i, expr, search):
		for j in i:
			match expr:
				case "anchor":
					if hasattr(j, "anchor") and j.anchor == search:
						return j
			if isinstance(j, Tag):
				return self._walk(j, expr, search)

	def __len__(self):
		return len(self._children)

	def __add__(self, i):
		self._children.append(i)

	def __sub__(self, i):
		if isinstance(i, int): self._children.remove(i)
		if isinstance(i, str) or isinstance(i, NHTag): self._children.pop(i)

	def insert_child(self, pos, name):
		self._children.insert(pos, name)

	def add_attr(self, name, value):
		setattr(self, name, value)

	def __str__(self):
		name = ansi.fstr("+ ", ansi.RED) if self._typedef else ""
		name += ansi.fstr("::"+self._name, ansi.YELLOW)

		for (i, j) in vars(self).items():
			if not i.startswith("_"): name += " " + ansi.fstr(i, ansi.MAGENTA) + ansi.fstr(" : ", ansi.YELLOW) + ansi.fstr(j, ansi.MAGENTA)

		return name

	def set_type(self, key, t):
		if isinstance(t, str): 
			t = getattr(ValueTypes, t)

		self._types[key] = t