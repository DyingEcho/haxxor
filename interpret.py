# haxxor by @DyingEcho
# Copyright ©2017 @DyingEcho. All rights reserved.

import sys
import exec
import error

tags = {}
prefixes = ["$", "#"]
currentLine = 0

args = sys.argv
try:
	script = args[1]
except IndexError:
	error.warn("No input file specified, assuming ./script.hx")
	script = "script.hx"
try:
	writeOut = args[2].lower()
	writeOut = True if writeOut == "true" else False
except IndexError:
	writeOut = False  # writeout not specified

with open(script, "r") as f:
	tasks = f.read().split("\n")

for task in tasks:
	if task.startswith("tag"):
		task = task.split(' ')
		tags[task[1]] = currentLine

	currentLine += 1

tasks.append("END")


def parse(usrtask):
	global prefixes
	global currentLine

	if usrtask.startswith("disp"):
		exec.disp(usrtask.strip("disp ").strip('"'))

	elif usrtask.startswith("assn"):
		usrtask = usrtask[5:]
		if usrtask.startswith("str"):
			usrtask = usrtask[4:]
			vartype = "str"
		elif usrtask.startswith("int"):
			usrtask = usrtask[4:]
			vartype = "int"
		elif usrtask.startswith("in"):
			usrtask = usrtask[3:]
			vartype = "in"
		elif usrtask.startswith("del"):
			usrtask = usrtask[4:]
			vartype = "del"
		else:
			error.error("Type to assign not recognised!")

		usrtask = usrtask.split(' "') if vartype != "int" else usrtask.split(" ")
		name = usrtask[0]
		value = usrtask[1].strip('"') if vartype != "del" else ""
		exec.assn(vartype, name, value)

	elif usrtask.startswith("wait"):
		try:
			length = int(usrtask.split(" ")[1])
		except ValueError:
			error.error("Parameter 1 to wait must be an integer")
		exec.wait(length)

	elif usrtask.startswith("strop"):
		usrtask = usrtask[6:]
		if usrtask.startswith("add"):
			usrtask = usrtask[4:]
			opType = "add"
		else:
			error.error("Strop command not recognised.")

		usrtask = usrtask.split(' ')
		firstVar = usrtask[0]
		secondVar = usrtask[1]

		exec.strop(opType, firstVar, secondVar)

	elif usrtask.startswith("goto"):
		global tags
		usrtask = usrtask.split(" ")
		goToLine = int(tags[usrtask[1]])

		currentLine = goToLine  # Change the line the interpreter will pass to the relevant tag
	elif usrtask == "END":
		exit()


currentLine = 0  # Reset to 0 so while loop starts from beggining
while currentLine < len(tasks):
	parse(tasks[currentLine])
	currentLine+=1
