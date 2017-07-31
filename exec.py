# haxxor by @DyingEcho
# Copyright ©2017 @DyingEcho. Some rights reserved.
# Licensed under the MIT License.

usrvars = {}

def disp(text):
	global usrvars
	if text.startswith("$"):
		print(usrvars[text])
	else:
		print(text)

def assn(vartype, name, value):
	global usrvars

	if vartype == "str":
		usrvars["$" + name] = value
