# haxxor by @DyingEcho
# Copyright ©2017 @DyingEcho. Some rights reserved.
# Licensed under the MIT License.

import error

usrvars = {}
prefixes = ["$", "#"]
tags = {}


def disp(text):
	global prefixes
	global usrvars

	isVar = 0
	for prefix in prefixes:
		if text.startswith(prefix): isVar += 1

	if isVar > 0:
		try:
			print(str(usrvars[text]))
		except KeyError:
			print("ERROR: String " + text + " not found.")
			exit()
	else:
		print(text)


def assn(vartype, name, value):
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

def strop(opType, firstVar, secondVar):
	if opType == "add":
		usrvars[firstVar] = usrvars[firstVar] + usrvars[secondVar]
