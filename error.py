# haxxor by @DyingEcho
# Copyright ©2017 @DyingEcho. All rights reserved.
from sys import exit

def error(msg, line, doExit=True):
	print("ERROR (ln " + str(line) + "): " + msg)
	if doExit: exit(1)

def warn(msg, line):
	print("WARN (ln " + str(line) + "): " + msg)
