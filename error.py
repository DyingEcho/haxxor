# haxxor by @DyingEcho
# Copyright ©2017 @DyingEcho. Some rights reserved.

def error(msg):
	from interpret import currentLine
	print("ERROR (ln " + str(currentLine) + "): " + msg)
	exit(1)

def warn(msg):
	from interpret import currentLine
	print("WARN (ln " + str(currentLine) + "): " + msg)