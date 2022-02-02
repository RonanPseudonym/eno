import cli.ansi as ansi
from datetime import datetime
import yaml, textwrap, os, re

# I am so, so sorry for this mess of a file

errors = yaml.safe_load(open("eno/yaml/err.yaml", "r"))
syserrors = yaml.safe_load(open("eno/yaml/syserr.yaml", "r"))

def output(text, color):
	print(ansi.fstr("=> " + text, color))

def err(name, file, line_pos, line_num, txt_line, **kwargs):
	highlight_color = ansi.RED
	highlight_bg = ansi.BG_RED

	if errors[name]["code"] < 200 and errors[name]["code"] >= 100:
		highlight_color = ansi.YELLOW
		highlight_bg = ansi.BG_YELLOW

	output(ansi.fstr(file, ansi.BOLD)+":"+str(line_num)+":"+str(line_pos[0])+" "+ansi.fstr(errors[name]["type"]+":"+ansi.fstr(name, ansi.BOLD), highlight_color), "")
	
	formatted_text = str()
	for i in range(len(txt_line)):
		if i >= line_pos[0] and i <= line_pos[1]:
			formatted_text += ansi.fstr(ansi.fstr(txt_line[i], highlight_bg), ansi.BOLD)
		else:
			formatted_text += txt_line[i]

	width = os.get_terminal_size()[0] - 20

	print("\t"+re.sub(r"[\n\t]*", "", formatted_text))
	print(ansi.fstr("\t"+"┌"+"─"*(line_pos[0] - txt_line.count("\t") - 1)+"┴"+"─"*(os.get_terminal_size()[0] - 16 - (line_pos[0] + 2 - txt_line.count("\t")))+"┐", highlight_color))

	errname = errors[name]["message"].replace("{cchar}", txt_line[line_pos[0]:line_pos[1]+1])
	
	tooltip = None

	if "tooltip" in errors[name]:
		tooltip = errors[name]["tooltip"]

	for i in kwargs:
		errname = errname.replace("{"+i+"}", kwargs[i])

		if tooltip:
			tooltip = tooltip.replace("{"+i+"}", kwargs[i])

	print(ansi.fstr("\t│ ", highlight_color)+ansi.fstr(errname, ansi.BOLD) + " "*(width - len(errname)) + ansi.fstr(" │", highlight_color))

	if tooltip != None:
		wrapper = textwrap.TextWrapper(width = width)
		for i in wrapper.wrap(text=tooltip):
			print(ansi.fstr("\t│ ", highlight_color)+i+" "*(width - len(i))+ansi.fstr(" │", highlight_color))

	print(ansi.fstr("\t└"+("─"*(width + 2))+"┘", highlight_color))

	if errors[name]["code"] >= 200:
		print()
		quit()

# def serr(name, arg = "ARG_ERR", arg2 = "ARG_ERR2"):
# 	self.err(name, "cmd_line", 0, )
# 	output("Error "+syserrors[name]["type"]+":"+ansi.fstr(name, ansi.BOLD), ansi.RED)
# 	print(ansi.fstr("\t"+syserrors[name]["message"].replace("{arg}", arg).replace("{arg2}", arg2), ansi.BOLD))
	
# 	if "tooltip" in syserrors[name]:
# 		wrapper = textwrap.TextWrapper(width = os.get_terminal_size()[0] - 8)
# 		for i in wrapper.wrap(text=syserrors[name]["tooltip"]):
# 			print("\t"+i)

# 	if "fatal" in syserrors[name] and syserrors[name]["fatal"]:
# 		print(ansi.fstr("\n\tFatalError: Program terminated", ansi.RED))
# 		quit()

def warning(text):
	output(text, ansi.YELLOW)

def ok(text):
	output(text, ansi.GREEN)

def info(text):
	output(text, ansi.CYAN)