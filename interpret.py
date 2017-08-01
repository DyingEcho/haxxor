# haxxor by @DyingEcho
# Copyright ©2017 @DyingEcho. All rights reserved.

import sys
import exec
import error

args = sys.argv
script = args[1]
writeOut = args[2].lower()
writeOut = True if writeOut == "true" else False

with open(script, "r") as f:
	tasks = f.read().split("\n")


def parse(usrtask):
	if usrtask.startswith("disp"):
		exec.disp(usrtask.strip("disp ").strip('"'))

	elif usrtask.startswith("assn"):
		usrtask = usrtask[5:]
		if usrtask.startswith("str"):
			usrtask = usrtask[4:]
			vartype = "str"
		elif usrtask.startswith("in"):
			usrtask = usrtask[3:]
			vartype = "in"
		else:
			error.error("Type to assign not recognised!")
		usrtask = usrtask.split(' "')
		name = usrtask[0]
		value = usrtask[1].strip('"')
		exec.assn(vartype, name, value)

	elif usrtask.startswith("wait"):
		try:
			length = int(usrtask.split(" ")[1])
		except ValueError:
			error.error("Parameter 1 to wait must be an integer")
		exec.wait(length)

for task in tasks: parse(task)
