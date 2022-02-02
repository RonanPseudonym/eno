import cli
from parse.tokens.dommer import *
from parse.tokens.tagger import *

class Dommer:
	def __init__(self, filename, tagsoup):
		self.tagsoup = tagsoup
		self.filename = filename
		self.pos = 0

		self.dom = Tag("dom")

	def l(self):
		return len(self.tagsoup)

	def advance(self):
		self.pos += 1

		if self.pos >= self.l(): 
			return None
		return self.tagsoup[self.pos]

	def peek(self):
		if self.pos + 1 >= self.l(): 
			return None
		return self.tagsoup[self.pos + 1]

	def current(self):
		return self.tagsoup[self.pos]

	def open_walk(self, c, find):
		if find and c._open: return c

		for i in c:
			if isinstance(i, Tag):
				x = self.open_walk(i, find)
				if x != None: return x

				if i._open and not find: return c
				if i._open and find:     return i

	def build_demitag(self, t):
		tag = Demitag(repr(t.name))

		for (i, j) in t.settings.items():

			ty = "NAME"

			match type(j).__name__:
				case "CascadingFallback":
					tag.add_attr(repr(i), j)
					continue
				case "String": ty = "STRING"
				case "Input": ty = "INPUT"
				case "Output": ty = "OUTPUT"
				case "Snippet": ty = "SNIPPET"

			tag.set_type(repr(i), ty)
			tag.add_attr(repr(i), repr(j))

		if t.is_typedef: tag._typedef = True

		return tag

	def build_tag(self, t):
		tag = Tag(repr(t.name))

		for (i, j) in t.settings.items():

			ty = "NAME"

			match type(j).__name__:
				case "CascadingFallback":
					tag.add_attr(repr(i), j)
					continue
				case "String": ty = "STRING"
				case "Input": ty = "INPUT"
				case "Output": ty = "OUTPUT"
				case "Snippet": ty = "SNIPPET"

			tag.set_type(repr(i), ty)
			tag.add_attr(repr(i), repr(j))

		if t.is_typedef: tag._typedef = True

		return tag

	def err(self, name, **kwargs):
		cli.err(name, self.filename, (self.current().start, self.current().end), self.current().line, self.current().line_txt, **kwargs)

	def walk(self):
		i = self.current()

		if type(i) == NHTag:
			if not i.can_close:
				self.open_walk(self.dom, True) + self.build_demitag(i)
			elif i.closing_tag:
				if repr(i.name) != self.open_walk(self.dom, True)._name:
					self.err("InvalidTagClosing", copen = self.open_walk(self.dom, True)._name, cclose = repr(i.name))
				a = self.open_walk(self.dom, True)

				self.open_walk(self.dom, False)._open = True
				a._open = False
			else:
				a = self.open_walk(self.dom, True)
				a + self.build_tag(self.current())
				a._open = False

		else: self.open_walk(self.dom, True) + repr(i)

		# ==========

		if self.advance() != None:
			self.walk()
		else:
			cli.ok("Converted "+self.filename+" to DOM")

	def generate_nodes(self, current_node, current_tag):
		for i in current_tag:
			n = cli.tree.Node(str(i) if isinstance(i, Tag) or isinstance(i, Demitag) else cli.ansi.GREEN + i.replace("\n", cli.ansi.CYAN + "\\n"+cli.ansi.GREEN) + cli.ansi.RESET)
			current_node.children.append(n)

			if isinstance(i, Tag): self.generate_nodes(n, i)

		return current_node

	def pretty_print(self):
		cli.tree.Tree(self.generate_nodes(cli.tree.Node(str(self.dom)), self.dom))