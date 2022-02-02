BLACK = "\u001b[40m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"
BLUE = "\u001b[34m"
MAGENTA = "\u001b[35m"
CYAN = "\u001b[36m"
WHITE = "\u001b[37m"

BBLACK = "\u001b[30m"
BRED = "\u001b[31m"
BGREEN = "\u001b[32m"
BYELLOW = "\u001b[33m"
BBLUE = "\u001b[34m"
BMAGENTA = "\u001b[35m"
BCYAN = "\u001b[36m"
BWHITE = "\u001b[37m"

BG_BRED = "\u001b[41;1m"
BG_RED = "\u001b[41m"

BG_YELLOW = "\u001b[43m"
BG_MAGENTA = "\u001b[45m"
BG_BLUE = "\u001b[44m"
BG_CYAN = "\u001b[46m"
BG_GREEN = "\u001b[42m"

BOLD = "\u001b[1m"
UNDERLINE = "\u001b[4m"

RESET = "\u001b[0m"

def fstr(text, color, light = False):
	if light: color += ";1m"
	return color + str(text) + RESET