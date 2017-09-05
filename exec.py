# haxxor by @DyingEcho
# Copyright ©2017 @DyingEcho. All rights reserved.
# Licensed under the MIT License.

import error
import parse

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

	if ' ' in name or '$' in name or '#' in name: error.warn("Variable name contains special character!", 0)

	if vartype == "str":
		if not isinstance(value, str): error.error("Can't assign a non-string as 'str'!", 0)
		usrvars["$" + name] = value

	if vartype == "num":
		if not isinstance(value, int) and not isinstance(value, float): error.error("Can't assign a non-int as 'int'!", 0)
		usrvars["#" + name] = value

	if vartype == "lst":
		usrvars["=" + name] = []

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

	try:
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
			try:
				fileContent = fileContent + "\n" + parse.getLiteral(param)
			except TypeError:
				error.error("Can't understand what to write!", 0)
			file.write(fileContent)
	except FileNotFoundError:
		error.error("No such file!", 0)


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


def lop(action, list, param):
	if action == "append":
		try:
			usrvars[list].append(parse.getLiteral(param))
		except KeyError:
			error.error("No such list " + list, 0)

	elif action == "pop":
		try:
			usrvars[list].pop(parse.getLiteral(param))
		except KeyError:
			error.error("No such list " + list, 0)
		except IndexError:
			error.error("List index out of range for " + list + " with " + str(len([usrvars[list]])) + " items.", 0)

	elif action == "ins":
		param = param.split(" ", 1)
		try:
			usrvars[list].insert(parse.getLiteral(param[0]), parse.getLiteral(param[1]))
		except KeyError:
			error.error("No such list " + list, 0)
