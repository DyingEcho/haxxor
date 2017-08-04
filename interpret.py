# haxxor by @DyingEcho
# Copyright 2017 @DyingEcho. All rights reserved.

import sys
import exec
import error

args = sys.argv
try:
	script = args[1]
except IndexError:
	print("No input file specified, assuming script.hx")
	script = "script.hx"
try:
	writeOut = args[2].lower()
	writeOut = True if writeOut == "true" else False
except IndexError:
	writeOut = False


with open(script, "r") as f:
	tasks = f.read().split("\n")

linePointer = 0 #Which line we are on

lastEvaluation = False #Tracks what the result of the last if statement is, this is used in the else statement

def findGotoTagLine(tagName):
	i = 0
	for task in tasks:
		if task.startswith("tag"):
			if tagName == task.split(" ")[1]:
				return i
		i+=1
	return -1

def parse(usrtask):
	global linePointer
	global lastEvaluation

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
		if vartype != "del" and vartype != "in":
			value = usrtask[1].strip('"')
		else:
			value = ""

		exec.assn(vartype, name, value)

	elif usrtask.startswith("wait"):
		try:
			length = int(usrtask.split(" ")[1])
		except ValueError:
			error.error("Parameter 1 to wait must be an integer")
		else:
			exec.wait(length)

	elif usrtask.startswith("if"):
		tsk = usrtask.split(" ")#This will split up the arugments, however, this will also split any strings with spaces
		tsk.pop(0)

		validComparitors = [">","<","=="]

		iii = 0#Current index
		for t in tsk: #For every argument inside the if statement
			if t[0] == "\"" and tsk[iii+1] not in validComparitors: #If its a string and the next value is not a comparitor
				tsk[iii]+=tsk[iii+1] #Concatinate the two strings that would have split from the spaces
			iii+=1

		checkInts = [0, 2]  # This is there incase you add multiple variable checking later on
		for asdf in checkInts:  # For every possible index for an argument
			if tsk[asdf][0] == "$" or tsk[asdf][0] == "#":
				tsk[asdf] == exec.usrvars[tsk[asdf]]  # Set the comparitor value to the value of the variable

		evaluation=False #Weather or not the statement is true
		
		if tsk[1] == ">":#Probaly more elagant way to do this but good enough...

			
			if tsk[0] > tsk[2]:
				evaluation=True
		elif tsk[1] == "<":
			if tsk[0] < tsk[2]:
				evaluation=True
		elif tsk[1] == "==":
			if tsk[0] == tsk[2]:
				evaluation=True
		lastEvaluation = evaluation
		if evaluation:
			l = findGotoTagLine(tsk[3])
			if l == -1:
				error.error("goto " + tsk[3] + " not found")
			else:
				linePointer=l
	elif usrtask.startswith("else"):
		if not tasks[linePointer-1].startswith("if"):
			error.error("If statement expected")
		if lastEvaluation:
			usrtask = usrtask[:5]
			l = findGotoTagLine(usrtask)
			if l == -1:
				error.error("goto " + usrtask + " not found")
			else:
				linePointer = l
	elif usrtask.startswith("goto"):
		l = findGotoTagLine(usrtask.split(" ")[1])
		
		if l == -1:
			error.error("goto " + usrtask.split(" ")[1] + " not found")
		else:
			linePointer=l
		
		
			
while linePointer < len(tasks): #TODO: Check if syntax is correct
	parse(tasks[linePointer])
	linePointer+=1

