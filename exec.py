# haxxor by @DyingEcho
# Copyright ©2017 @DyingEcho. All rights reserved.
# Licensed under the MIT License.

import error

usrvars = {}
prefixes = ["$", "#"]
tags = {}
file = None


def disp(text):
	print(text)


def assn(vartype, name, value):
	# Because this sets a variable that doesn't already exist, we have to do it the clunky way instead of getLiteral()
	global usrvars
	global prefixes

	for prefix in prefixes:
		if name.startswith(prefix) and vartype != "del": error.warn("Variable name contains special character!", 0)

	if vartype == "str":
		if not isinstance(value, str): error.error("Can't assign a non-string as 'str'!", 0)
		usrvars["$" + name] = value

	if vartype == "int":
		if not isinstance(value, int): error.error("Can't assign a non-int as 'int'!", 0)
		usrvars["#" + name] = value

	if vartype == "in":
		usrvars["$" + name] = input(value)

	if vartype == "del":
		exists = 0
		for prefix in prefixes:
			try:
				usrvars.pop(prefix + name)
			except KeyError:
				exists += 1
		if exists > 1:
			error.error("Variable " + name + " does not exist and so can't be deleted.", 0)


def wait(length):
	from time import sleep
	sleep(length / 1000)


def strop(opType, origin, param):
	if opType == "add":
		try:
			usrvars[origin] = usrvars[origin] + param
		except KeyError:
			error.error("Parameter 0 to 'strop add' must be a string variable", 0)
		except TypeError:
			error.error("All parameters to 'strop add' must be strings.", 0)


def flop(action, param):
	global usrvars
	global prefixes
	global file

	if action == "open":
		file = open(param, "a+")

	elif action == "close":
		file.close()

	elif action == "read":
		usrvars[param] = file.read()

	elif action == "owrite":
		file.write(param)

	elif action == "append":
		fileContent = file.read()
		fileContent = fileContent + "\n" + param
		file.write(fileContent)


def nop(action, origin, param):
	try:
		if action == "add":
			usrvars[origin] = usrvars[origin] + param
		elif action == "sub":
			usrvars[origin] = usrvars[origin] - param
		elif action == "div":
			usrvars[origin] = usrvars[origin] / param
		elif action == "mult":
			usrvars[origin] = usrvars[origin] * param
		elif action == "exp":
			usrvars[origin] = usrvars[origin] ^ param
		elif action == "mod":
			usrvars[origin] = usrvars[origin] % param
	except TypeError:
		error.error("All parameters to 'nop' must be integers.", 0)
	except KeyError:
		error.error("Parameter 1 to 'nop' must be an integer variable.", 0)