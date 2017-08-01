# haxxor by @DyingEcho
# Copyright ©2017 @DyingEcho. Some rights reserved.
# Licensed under the MIT License.

usrvars = {}

def disp(text):
	global usrvars
	if text.startswith("$"):
		try:
			print(usrvars[text])
		except KeyError:
			print("ERROR: String " + text + " not found.")
	else:
		print(text)

def assn(vartype, name, value):
	global usrvars
	if name.startswith("$"): print("WARN: Variable name contains special character!")

	if vartype == "str":
		usrvars["$" + name] = value
