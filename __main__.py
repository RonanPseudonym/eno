import parse, cli

data = cli.run()
match data["type"]:
	case "parse":
		path = data["args"][0]
		print(data)
		layers = data["attr"]["layers"]
		visible = "visible" in data["enabled"]

		output = None

		if layers >= 1:
			lexer = parse.Lexer(path)
			lexer.walk()

			output = lexer.lexemes

			if visible: 
				print()
				cli.info("Output of stage one (lexer):")
				lexer.pretty_print()
				print("\n")

		if layers >= 2:
			tagger = parse.Tagger(path, output)
			tagger.walk()

			output = tagger.tagsoup
			
			if visible: 
				print()
				cli.info("Output of stage two (tagger):")
				tagger.pretty_print()
				print("\n")

		if layers >= 3:
			dommer = parse.Dommer(path, output)
			dommer.walk()

			output = dommer.dom

			if visible: 
				print()
				cli.info("Output of stage three (dommer):")
				dommer.pretty_print()
				print("\n")