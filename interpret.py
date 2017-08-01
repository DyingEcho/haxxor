# haxxor by @DyingEcho
# Copyright ©2017 @DyingEcho. All rights reserved.

import sys
import exec

args = sys.argv
script = args[1]
writeOut = args[2].lower()
writeOut = True if writeOut == "true" else False #TODO: fix this!

print("Running file '" + script + "' (arg WriteOut is " + str(writeOut) + ")")
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
		else:
			print("Error: Type not recognised")
			print(usrtask)
			exit()
		usrtask = usrtask.split(' "')
		name = usrtask[0]
		value = usrtask[1].strip('"')
		exec.assn(vartype, name, value)
	elif usrtask.startswith("wait"):
		length = int(usrtask.split(" ")[1])
		exec.wait(length)

for task in tasks: parse(task)
