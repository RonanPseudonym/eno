import sys, yaml
import cli.log as log
from cli.log import err

cliopt = yaml.safe_load(open("eno/yaml/cli.yaml"))

def entry(d, i):
	for j in d["conf"]:
		if list(j.keys())[0] == i:
			return list(j.values())[0]
	return False

def serr(name, pos = (0, 0), **kwargs):
	err(name, "cmd_line", pos, 0, " ".join(sys.argv), **kwargs)

def run():
	if len(sys.argv) <= 1:
		serr("NoArgumentsSpecified")
	
	if not sys.argv[1] in cliopt:
		serr("InvalidArgument", arg=sys.argv[1], pos = (" ".join(sys.argv).index(sys.argv[1]), " ".join(sys.argv).index(sys.argv[1]) + len(sys.argv[1])))

	d = cliopt[sys.argv[1]]
	open_tag = None
	argcount = 0

	output = {
		"type": sys.argv[1],
		"args": [],
		"enabled": [],
		"attr": {}
	}

	for i in sys.argv[2:]:
		if i.startswith("--"):
			name = i.replace("--", "")

			if not entry(d, name):
				serr("InvalidArgument", arg = name, pos = (" ".join(sys.argv).index(i), " ".join(sys.argv).index(i) + len(i)))

			if "toggle" in entry(d, name) and entry(d, name)["toggle"]:
				output["enabled"].append(name)
			else:
				open_tag = name

		else:
			subargs = "str"

			if open_tag:
				subargs = entry(d, name)["type"]
			else:
				if argcount < len(d["args"]):
					subargs = list(d["args"].values())[argcount]
					argcount += 1
				else:
					serr("NoMoreArgumentsPossible", arg = i, pos = (" ".join(sys.argv).index(i), " ".join(sys.argv).index(i) + len(i)))

			subargs = subargs.split("[")
			if len(subargs) > 1: subargs[1] = [int(i) for i in subargs[1].replace("]","").split(";")]

			j = i

			match subargs[0]:
				case "int":
					if i.isnumeric():
						j = int(i)
						if len(subargs) > 1:
							if not (int(i) >= subargs[1][0] and int(i) <= subargs[1][1]):
								serr("IntegerOutOfRange", arg = i, arg2 = "-".join(list(map(str, subargs[1]))), pos = (" ".join(sys.argv).index(i), " ".join(sys.argv).index(i) + len(i)))
					else:
						serr("CommandLineIntegerInvalid", arg = i, pos = (" ".join(sys.argv).index(i), " ".join(sys.argv).index(i) + len(i)))

			if open_tag:
				output["attr"][open_tag] = j
				open_tag = None
			else:
				output["args"].append(j)


	if len(output["args"]) < len(d["args"]):
		serr("NotEnoughArguments", arg = str(len(d["args"])) + [" is"," are"][len(d["args"])>1], pos = (" ".join(sys.argv).index(i), " ".join(sys.argv).index(i)))
	if open_tag:
		serr("OptionalArgumentLeftOpen", arg = open_tag, pos = (" ".join(sys.argv).index(i), " ".join(sys.argv).index(i) + len(i)))

	for i in d["conf"]:
		iname = list(i.keys())[0]
		ival = list(i.values())[0]

		if not ("toggle" in ival and ival["toggle"]):
			if not iname in output["attr"]:
				output["attr"][iname] = ival["dflt"]

	return output
