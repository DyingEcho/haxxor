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

	for prefix in prefixes:
		if name.startswith(prefix): error.warn("Variable name contains special character!")

	if vartype == "str":
		usrvars["$" + name] = value

	if vartype == "int":
		usrvars["#" + name] = value

	if vartype == "in":
		usrvars["$" + name] = input(value)

	if vartype == "del":
		for prefix in prefixes:
			try:
				usrvars.pop(prefix + name)
			except KeyError:
				pass


def wait(length):
	from time import sleep
	sleep(length / 1000)


def strop(opType, origin, param):
	if opType == "add":
		usrvars[origin] = usrvars[origin] + param


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
