# Some (lots of) help from https://andrewlock.net/creating-an-ascii-art-tree-in-csharp/

class Node:
	def __init__(self, txt):
		self.txt = txt
		self.children = []

class Tree:
	CROSS = " ├─";
	CORNER = " └─";
	VERTICAL = " │ ";
	SPACE = "   ";

	def __init__(self, base):
		self.top_level_nodes = [base]

		for node in self.top_level_nodes:
			self.print_node(node, "")

	def print_node(self, node, indent):
		print(node.txt)

		for i in range(len(node.children)):
			child = node.children[i]
			is_last = i == len(node.children) - 1
			self.print_child_node(child, indent, is_last)

	def print_child_node(self, node, indent, is_last):
		print(indent, end = "")

		if is_last:
			print(self.CORNER, end = "")
			indent += self.SPACE
		else:
			print(self.CROSS, end = "")
			indent += self.VERTICAL

		self.print_node(node, indent)