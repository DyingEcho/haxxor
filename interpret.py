# haxxor by @DyingEcho
# Copyright ©2017 @DyingEcho. All rights reserved.

import sys
import exec
import error

tags = {}  # dictionary of tags. key is name, value is line number.
prefixes = ["$", "#"]  # so we can check if something is a variable
lastEvaluation #The state of the last if statement


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
		currentLine = goToLine  # Change the line the interpreter is reading
	elif usrtask.startswith("if"):
		task = usrtask.split(
			" ")  # This will split up the arugments, however, this will also split any strings with spaces
		task.pop(0)

		validComparitors = [">", "<", "=="]

		checkInts = [0, 2]  # This is there incase you add multiple variable checking later on
		for asdf in checkInts:  # For every possible index for an argument
			if task[asdf][0] in prefixes:
				task[asdf] = exec.usrvars[
					task[asdf]]  # Make it so the interpreter is comparing the values, not the variable name

		evaluation = False  # Weather or not the if statement is true

		i = 0  # Current index
		for t in task:  # For every argument inside the if statement, This will make sure any strings that where split with the .split gets rejoined
			try:#I have no clue why this works, it just works
				lst = task[i + 1][-1:]#The last character
				if t[0] == "\"" and lst == "\"":  # If its a string literal and the next value is also a string literal
					task[i] += task[i + 1]  # Concatinate the two strings that would have split from the spaces
					task.pop(i + 1)
			except IndexError:
				pass
			i+= 1

		if task[1] == ">":  # Probaly more elagant way to do this but good enough...
			if task[0] > task[2]:
				evaluation = True
		elif task[1] == "<": #If the user wants that if statemnt
			if task[0] < task[2]: #Then check the result
				evaluation = True #And set evaluation
		elif task[1] == "==":
			if task[0] == task[2]:
				evaluation = True

		lastEvaluation = evaluation
		if evaluation:
			l = int(tags[task[3]])
			currentLine = l #Set the current line to the goto line
			
	elif usrtask.startswith("else"):
		if not tasks[currentLine - 1].startswith("if"):  # If the last line was not if
			error.error("If statement expected")
		if not lastEvaluation:  # If the last eval was true
			usrtask = usrtask[5:]
			l = int(tags[usrtask])
			currentLine = l
	elif task == "END":
		exit()

currentLine = 0  # Reset to 0 due to its use in the original scan of the file for tags
while currentLine < len(tasks):  # While the line we're on is not the last:
	parse(tasks[currentLine])  # parse the task at the current line in tasks
	currentLine += 1  # Move on to the next line
