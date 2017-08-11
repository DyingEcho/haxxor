# haxxor by @DyingEcho
# Copyright ©2017 @DyingEcho. All rights reserved.

import sys
import exec
import error

tags = {}  # dictionary of tags. key is name, value is line number.
prefixes = ["$", "#"]  # so we can check if something is a variable



"""
STEP 1: EVALUATE ARGUMENTS
We read through system arguments passed to the interpreter to decide how to run our code.
"""
args = sys.argv  # get a string with everything after the command to run this interpreter
try:
	script = args[1]  # the location of the script to run
except IndexError:  # not specified
	error.warn("No input file specified, assuming ./script.hx")
	script = "script.hx"
try:
	writeOut = args[2].lower()  # do we write the meaning of the script to a python file or run it?
	writeOut = True if writeOut == "true" else False  # if the user says "true" set writeOut to True, otherwise False
except IndexError:  # not specified
	error.warn("WriteOut not specified, assuming False")
	writeOut = False



"""
STEP 2: GET LIST OF COMMANDS
We get a list of commands ('tasks') that we need to interpret into Python code to run or write to a file.
"""
try:
	with open(script, "r") as f:
		tasks = f.read().split("\n")  # create task list by splitting on newlines
except FileNotFoundError:  # no such file!
	error.error("File " + script + "not found")
except:
	error.error("Generic error reading file" + script)



"""
STEP 3: FIND TAGS
We create a dictionary of tags that we can goto later.
"""
currentLine = 0  # we use this to store the line number of any tags we find, by incrementing it each line
for task in tasks:
	if task.startswith("tag"):
		task = task.split(' ')
		tags[task[1]] = currentLine  # add entry to tags with key as tag name and value as line number

	currentLine += 1

tasks.append("END")  # so we know to end the script after a goto, otherwise we'd go back once script ended post-goto



"""
STEP 4: PARSE TASKS
We look at each task in order and do something based on it.
"""
def parse(task):
	global prefixes

	if task.startswith("disp"):  # displays a string
		exec.disp(task.strip("disp ").strip('"'))  # remove command and any quotation marks, then pass to exec.disp()

	elif task.startswith("assn"):  # assigns/deletes a variable
		task = task[5:]
		if task.startswith("str"):  # it's a string
			task = task[4:]
			vartype = "str"
		elif task.startswith("int"):  # it's an integer
			task = task[4:]
			vartype = "int"
		elif task.startswith("in"):  # we need user input for a string
			task = task[3:]
			vartype = "in"
		elif task.startswith("del"):  # deletes a variable
			task = task[4:]
			vartype = "del"
		else:
			error.error("Type to assign not recognised!")

		task = task.split(' "') if vartype != "int" else task.split(" ")  # split by space if type is int, otherwise by "
		name = task[0]  # name of the variab;e
		value = task[1].strip('"') if vartype != "del" else ""  # strip task[1] by " if type isn't del, assign to value
		exec.assn(vartype, name, value)  # pass to exec.assn()

	elif task.startswith("wait"):  # waits for a certain amount of time
		try:
			length = int(task.split(" ")[1])
		except ValueError:
			error.error("Parameter 1 to wait must be an integer")
		exec.wait(length)

	elif task.startswith("strop"):
		task = task[6:]
		if task.startswith("add"):
			task = task[4:]
			opType = "add"
		else:
			error.error("Strop command not recognised.")

		task = task.split(' ')
		firstVar = task[0]
		secondVar = task[1]

		exec.strop(opType, firstVar, secondVar)

	elif task.startswith("goto"):
		global tags
		task = task.split(" ")
		goToLine = int(tags[task[1]])

		for task in tasks[goToLine:]:
			parse(task)

	elif task == "END":
		exit()

for task in tasks:
	parse(task)
