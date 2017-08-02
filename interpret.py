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

linePointer = 0 #Which line we are on

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
	elif usrtask.startswith("if"):
		tsk = usertask.split(" ")#TODO: FIx this, it will trigger on strings with spaces
		usertask.pop(0)
		
		evaluation=False
		
		if tsk[1] == ">":#Probaly more elagant way to do this but good enough...
			checkInts = [0,2] #This is there incase you add multiple variable checking later on
			for asdf in checkInts:
				if tsk[asdf][0] == "$":
					tsk[asdf] == exec.usrvars[tsk[asdf]]
			
			if tsk[0] > tsk[2]:
				evaluation=True
		elif tsk[1] == "<":
			if tsk[0] < tsk[2]:
				evaluation=True
		elif tsk[1] == "==":
			if tsk[0] == tsk[2]:
				evaluation=True
		
		if evaluation:
			l = findGotoTagLine(tsk[3])
			if l == -1:
				pass #TODO: Throw error
			else:
				linePointer=l
	elif usrtask.startswith("goto"):
		l = findGotoTagLine(usrtask.split(" ")
		
		if l == -1:
				pass #TODO: Throw error
		else:
				linePointer=l
		
		
			
while linePointer <= len(tasks): #TODO: Check if syntax is correct
	parse[tasks[linePointer]]
	linePointer+=1

