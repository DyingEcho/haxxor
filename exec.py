# haxxor by @DyingEcho
# Copyright ©2017 @DyingEcho. Some rights reserved.
# Licensed under the MIT License.

usrvars = {}
import error

def disp(text):
	global usrvars
	if text.startswith("$"):
		try:
			print(usrvars[text])
		except KeyError:
			print("ERROR: String " + text + " not found.")
			exit()
	else:
		print(text)

def assn(vartype, name, value):
	global usrvars
	if name.startswith("$"): error.warn("Variable name contains special character!")

	if vartype == "str":
		usrvars["$" + name] = value

	if vartype == "in":
		usrvars["$" + name] = input(value)


def wait(length):
	from time import sleep
	sleep(length / 1000)