# haxxor by @DyingEcho
# Copyright ©2017 @DyingEcho. All rights reserved.
import error
import exec
from interpret import currentLine


def getLiteralList(objList, removeQuotes=True, exitIfMeaningless=True):
	import re  # we need regex to determine what is a variable and what is a literal
	import itertools
	regex = '[$#]\w*'  # https://regex101.com/r/is4StU/4 for explanation


	variables = re.findall(regex, objList)  # list of variables
	counter = 0
	for var in variables:
		try:
			var = exec.usrvars[var]
		except KeyError:
			error.error("Could not find variable " + var, currentLine)
		if isinstance(var, str):  # it's a string
			var = var if removeQuotes else '"' + var + '"'  # if not removeQuotes, add quotes to each end

		variables[counter] = var  # replace the variable names with the values
		counter += 1


	literals = re.split(regex, objList)  # list of literals
	counter = 0
	listStartsWith = 0  # so we know how to properly merge the 2 lists once we're done
	modLiterals = []  # we will modify this in the for loop to prevent interference when removing list items

	for obj in literals:  # sometimes we get empty strs with the literal split, this removes them
		literals[counter] = obj.strip(" ")  # remove any spaces at the start or end
		if obj != "" and obj is not None:
			modLiterals.append(literals[counter])  # only append if it's not empty
		else:
			listStartsWith += 1  # it's empty so we can increment it - trust my logic on this
		counter += 1
	literals = modLiterals  # update variabes safely outside the for loop

	if listStartsWith > 0: listStartsWith = "lit"  # trust my logic!

	counter = 0
	for obj in literals:
		if obj.startswith('"') and obj.endswith('"'):  # it's a string
			literals[counter] = obj.strip('"') if removeQuotes else obj  # remove any quotes from front and back
		else:  # it's either an int or unrecognised
			try:
				literals[counter] = int(obj)  # try to int() it, if it's impossible we get ValueError
			except ValueError:
				if exitIfMeaningless: error.error("Could not get anything meaningful from " + obj, currentLine, doExit=False)  # not a string, not an int
				return False
		counter += 1


	ret = list(
		filter(None, sum(itertools.zip_longest(literals, variables), ()))) if listStartsWith == "lit" \
		else list(filter(None, sum(itertools.zip_longest(variables, literals), ())))  # alternately merge the 2 lists
	return ret


def getLiteral(unParsedObj, removeQuotes=True, exitIfMeaningless=True):
	try:
		return getLiteralList(unParsedObj, removeQuotes=removeQuotes, exitIfMeaningless=exitIfMeaningless)[0]  # for getting one result only
	except TypeError:  # it returns 'false'
		return getLiteralList(unParsedObj, removeQuotes=removeQuotes, exitIfMeaningless=exitIfMeaningless)