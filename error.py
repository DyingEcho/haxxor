# haxxor by @DyingEcho
# Copyright ©2017 @DyingEcho. Some rights reserved.

def error(msg, line, doExit=True):
	print("ERROR (ln " + str(line) + "): " + msg)
	if doExit: exit(1)

def warn(msg, line):
	print("WARN (ln " + str(line) + "): " + msg)
