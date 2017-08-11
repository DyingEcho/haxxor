# haxxor by @DyingEcho
# Copyright ©2017 @DyingEcho. All rights reserved.

import sys
import exec
import error

tags = {}  # dictionary of tags. key is name, value is line number.
prefixes = ["$", "#"]  # so we can check if something is a variable
lastEval = False
lastTaskWasIf = False



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
	global currentLine

	if task.startswith("disp"):  # displays a string
		exec.disp(getValue(task.strip("disp ")))  # remove command and any quotation marks, then pass to exec.disp()

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
		value = getValue(task[1]) if vartype != "str" else getValue('"' + task[1])
		exec.assn(vartype, name, value)  # pass to exec.assn()

	elif task.startswith("wait"):  # waits for a certain amount of time
		length = getValue(task.split(" ")[1])  # split by spaces and take the second part (the time to wait)
		exec.wait(length)

	elif task.startswith("strop"):  # string operations
		task = task[6:]  # Get rid of the 'strop ' at the task start
		if task.startswith("add"):  # concatenate strings
			task = task[4:]
			opType = "add"
		else:
			error.error("Strop command not recognised.")

		task = task.split(' ')
		firstVar = getValue(task[0])
		secondVar = task[1]

		exec.strop(opType, firstVar, secondVar)

	elif task.startswith("goto"):
		global tags
		task = task.split(" ")
		goToLine = int(tags[task[1]])
		currentLine = goToLine  # Change the line the interpreter is reading

	elif task.startswith("if"):
		global lastEval
		global lastTaskWasIf

		lastTaskWasIf = True
		task = task[3:]
		task = task.split(' |> ', 1)  # Split on first occurence of "|> "
		"""
		By this point, if we started with 
			"if $hello == "hi": goto hi"
		we would now have
			["$hello == "hi",  "goto hi"]
		"""
		clause = task[0]  # "$hello == "hi""
		operation = task[1]  # "goto hi"

		clause = clause.split(" ")  # ["$hello", "==", ""hi""]
		counter = 0
		for part in clause:  # for every item in list ["$hello", "==", ""hi""]
			for prefix in prefixes:
				if part.startswith(prefix):
					if prefix == "$":
						clause[counter] = '"' + str(exec.usrvars[part]) + '"'  # It's a string so give it quotes, also see else
					else:
						clause[counter] = str(exec.usrvars[part])  # replace variables with values - ["hi", "==", ""hi""]
		counter += 1
		clause = " ".join(clause)  # ""hi" == "hi""

		clauseCheck = eval(clause)  # use Python's boolean evaluation and store bool result in clauseCheck

		if clauseCheck:
			lastEval = True
			parse(operation)  # do the operation
		else:
			lastEval = False

	elif task.startswith("else"):
		task = task[8:]  # remove 'else |> '
		if not lastTaskWasIf:
			error.error("Else statement must be after if")
		if not lastEval:
			parse(task)

	elif task.startswith("flop"):
		task = task[5:]  # remove 'flop ' from start of task
		if task.startswith("open"):
			task = task[5:]
			action = "open"
		if task.startswith("close"):
			task = task[6:]
			action = "close"
		if task.startswith("read"):
			task = task[5:]
			action = "read"
		if task.startswith("owrite"):
			task = task[7:]
			action = "owrite"
		if task.startswith("append"):
			task = task[7:]
			action = "append"

		exec.flop(action, task)  # pass to flop with the action and the parameter (str, path or nothing)


	elif task == "END":
		exit()



def getValue(item):
	for prefix in prefixes:
		if item.startswith(prefix):
			return exec.usrvars[item]
	if item.startswith('"') and item.endswith('"'):
		item = str(item.strip('"'))
		return item
	try:
		item = int(item)
		return item
	except ValueError:
		error.error("Item" + str(item) + " could not be resolved into anything meaningful.")



currentLine = 0  # Reset to 0 due to its use in the original scan of the file for tags
try:
	while currentLine < len(tasks):  # While the line we're on is not the last:
		parse(tasks[currentLine])  # parse the task at the current line in tasks
		currentLine += 1  # Move on to the next line
except KeyboardInterrupt:
	exit()