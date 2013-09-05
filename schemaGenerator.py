#!/usr/bin/python
#coding=UTF-8

############################################
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#	Anti Räis, 2012-2013
#
############################################

############################################
# CoCoVila schema generator
#
# Generates schema from CSV file.
############################################

import sys
import collections

#Settings
class DefaultSettings:
	readFromFile		= "out.csv"
	writeToFile			= "result.syn"
	gradedSecLevels		= 5
	abbrPosition		= 0
	fullNamePosition	= 1
	invColumn			= 2
	effColumn			= invColumn + gradedSecLevels
	invDivider			= 1000
	effDivider			= 100
	maintDivider		= invDivider*2
	showskipped			= False

	def __str__(self):
		fields = [
			attr
			for attr in dir(self)
				if not isinstance(attr, collections.Callable) and not attr.startswith("__")
		]

		result = "{:*^35}\n".format('Settings')
		for field in fields:
			result += "{:<20}{}\n".format(str(field), str(getattr(self, field)))
		return result

#Command line parameters
class CLIParams:
	help				= ['-h', '--help']
	showskipped			= ['-s', '--showskipped']
	readFromFile		= ['-r', '--readFromFile']
	writeToFile			= ['-w', '--writeToFile']
	gradedSecLevels		= ['-g', '--gradedSecurityLevels']
	abbrPosition		= ['-a', '--abbrevationPosition']
	fullNamePosition	= ['-f', '--fullNamePosition']
	invColumn			= ['-i', '--investmentColumn']
	effColumn			= ['-e', '--effectColumn']
	invDivider			= ['-id', '--investmentDivider']
	effDivider			= ['-ed', '--effectDivider']
	maintDivider		= ['-md', '--maintainabilityDivider']

	def getAllCLIParamValues(self):
		fields = [
			attr
			for attr in dir(self)
				if not isinstance(attr, collections.Callable) and not attr.startswith("__")
		]
		fields.remove(self.getAllCLIParamValues.__name__)

		result = []
		for field in fields:
			result = result + getattr(self, field)

		return result

def object(i, abbr, fullName, invest, effect, maint):
	x_pos = 30
	y_pos = 30
	iLvlSit = 0

	string = ""
	string = string + '	<object name="MeasureGroup_'+str(i)+'" type="MeasureGroup" static="false">\n'
	string = string + '		<properties x="'+str(x_pos)+'" y="'+str(i*y_pos)+'" xsize="1.0" ysize="1.0" strict="false"/>\n'
	string = string + '		<fields>\n'
	string = string + '		<field name="sCode" type="String" value="'+abbr+'"/>\n'
	string = string + '		<field name="sDescription" type="String" value="'+fullName+'"/>\n'
	string = string + '		<field name="vdInvest" type="double[]" value="'+invest+'"/>\n'
	string = string + '		<field name="vdEffect" type="double[]" value="'+effect+'"/>\n'
	string = string + '		<field name="vdMaintn" type="double[]" value="'+maint+'"/>\n'
	string = string + '		<field name="iLvlSit" type="int" value="'+str(iLvlSit)+'"/>\n'
	string = string + '		<field name="iLvlReq" type="int"/>\n'
	string = string + '		</fields>\n'
	string = string + '	</object>\n'
	return string

def printTemplateHeader():
	return '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE scheme SYSTEM "scheme.dtd">\n<scheme package="optimization">\n'

def printTemplateFooter():
	return '</scheme>'

def getValue(value, invDivider):
	valueSeparator = "%%"
	value = replaceAll(value)

	if value == '':
		return str(0.0)+valueSeparator

	try:
		val = float(value)/invDivider
	except:
		print("ERROR: Can't convert {} to float!".format(value))
		raise

	return str(val)+valueSeparator

def replaceAll(str):
	# First "space" char replacement is unknown character
	return str.replace("€", "").replace("\n", "").replace(" ", "").replace(" ", "")

def escapeXMLChars(str):
	return str.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def author():
	print("Optimization schema generator for CoCoVilA")
	print("Written by Anti Räis, 2012 GPLv3")
	print("")

def getValues(startColumn, secLevels, elems, divider):
	result = ""
	for i in range(secLevels):
		result = result + getValue(elems[startColumn+i], divider)
	return result

def getParamPos(tacks, args):
	for tack in enumerate(tacks):
		if str(tack[-1]) in args:
			return tack
	return False

def getInvalidParamPos(tacks, args):
	for tack in enumerate(tacks):
		if not str(tack[-1]) in args:
			return tack
	return False

def printHelp():
	joiner = ', '
	print("Usage: {} [OPTIONS]\n".format(programName))
	print("DESCRIPTION")
	print("\tGenerates schema for CoCoVila from CSV file.\n")
	print("\t{}\n\t\t{}\n".format(joiner.join(cliParams.help), "You are looking at it. :)"))
	print("\t{}\n\t\t{}\n".format(joiner.join(cliParams.showskipped), "Displays skipped lines from input file"))
	print("\t{}\n\t\t{}\n".format(joiner.join(cliParams.readFromFile), "Input CSV file to read from"))
	print("\t{}\n\t\t{}\n".format(joiner.join(cliParams.writeToFile), "Sets the output file name. CoCoVila uses extension .syn"))
	print("\t{}\n\t\t{}\n".format(joiner.join(cliParams.gradedSecLevels), "Sets number of columns or CSV values to read sequently"))
	print("\t{}\n\t\t{}\n".format(joiner.join(cliParams.abbrPosition), "Sets the abbrevation column position"))
	print("\t{}\n\t\t{}\n".format(joiner.join(cliParams.fullNamePosition), "Sets the full name column position"))
	print("\t{}\n\t\t{}\n".format(joiner.join(cliParams.invColumn), "Sets the first investment column. Reads as many parameters as defined by graded security level"))
	print("\t{}\n\t\t{}\n".format(joiner.join(cliParams.effColumn), "Sets the first effectiveness column. Reads as many parameters as defined by graded security level"))
	print("\t{}\n\t\t{}\n".format(joiner.join(cliParams.invDivider), "Sets the investment value divider. All investment values are divided by that value and result used in output"))
	print("\t{}\n\t\t{}\n".format(joiner.join(cliParams.effDivider), "Sets the effectiveness value divider. All effectiveness values are divided by that value and result used in output"))
	print("\t{}\n\t\t{}\n".format(joiner.join(cliParams.maintDivider), "Sets the maintainability value divider. All maintainability values are divided by that value and result used in output"))
	print("AUTHOR")
	print("\tWritten by Anti Räis <antirais@gmail.com>\n")
	print("COPYRIGHT")
	print("\tLicense GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.")
	print("\tThis  is  free  software:  you  are  free to change and redistribute it.")
	print("\tThere is NO WARRANTY, to the extent permitted by law.")

	sys.exit(0)

# Warning! Bad code ahead! Fix me!
def parseCLIParams(argv):
	if len(argv) == 0:
		return

	if getParamPos(cliParams.help, argv):
		printHelp()

	pos = getParamPos(cliParams.showskipped, argv)
	if pos:
		settings.showskipped = True
		argv.remove(pos[1])

	for arg in zip(argv[0::2], argv[1::2]):
		if str(arg[0]) in cliParams.readFromFile:
			settings.readFromFile = arg[1]
		elif str(arg[0]) in cliParams.writeToFile:
			settings.writeToFile = arg[1]
		elif str(arg[0]) in cliParams.gradedSecLevels:
			try:
				level = int(arg[1])
			except:
				print("ERROR! Graded security level must be an integer!")
				raise
			settings.gradedSecLevels = level
		elif str(arg[0]) in cliParams.abbrPosition:
			try:
				pos = int(arg[1])
			except:
				print("ERROR! Abbrevation position must be an integer!")
				raise
			settings.abbrPosition = pos
		elif str(arg[0]) in cliParams.fullNamePosition:
			try:
				pos = int(arg[1])
			except:
				print("ERROR! Full name position must be an integer!")
				raise
			settings.fullNamePosition = pos
		elif str(arg[0]) in cliParams.invColumn:
			try:
				pos = int(arg[1])
			except:
				print("ERROR! Investment column position must be an integer!")
				raise
			settings.invColumn = pos
		elif str(arg[0]) in cliParams.effColumn:
			try:
				pos = int(arg[1])
			except:
				print("ERROR! Effect column position must be an integer!")
				raise
			settings.effColumn = pos
		elif str(arg[0]) in cliParams.invDivider:
			try:
				pos = int(arg[1])
			except:
				print("ERROR! Investment divider must be an integer!")
				raise
			settings.invDivider = pos
		elif str(arg[0]) in cliParams.effDivider:
			try:
				pos = int(arg[1])
			except:
				print("ERROR! Effect divider must be an integer!")
				raise
			settings.effDivider = pos
		elif str(arg[0]) in cliParams.maintDivider:
			try:
				pos = int(arg[1])
			except:
				print("ERROR! maintainability divider must be an integer!")
				raise
			settings.maintDivider = pos
		else:
			print("Unknown argument: {}".format(arg[1]))
			print("")
			printHelp()
	return

############################################
# Main program
############################################
settings = DefaultSettings()
cliParams = CLIParams()
author()
programName = sys.argv[0]
parseCLIParams(sys.argv[1:])
print(settings)

try:
	rf = open(settings.readFromFile, 'r')
except:
	print("ERROR! Cannot find input file named {}".format(settings.readFromFile))
	raise
try:
	wf = open(settings.writeToFile, 'w')
except:
	print("ERROR! Cannot open file to write named {}".format(settings.writeToFile))
	raise

wf.write(printTemplateHeader())

iter = 0
for line in rf.readlines():
	elems = line.split(',')

	#Check if this is a valid row, not a header row containing now useful information
	elem = replaceAll(elems[settings.invColumn])
	if not elem.isdigit() or elems[settings.fullNamePosition] == '' or elems[settings.abbrPosition] == '':
		if settings.showskipped:
			print("Skipping line: {}".format(line.replace('\n', '')))
		continue

	abbr = replaceAll(escapeXMLChars(elems[settings.abbrPosition]))
	fullName = escapeXMLChars(elems[settings.fullNamePosition])
	invest = getValues(settings.invColumn, settings.gradedSecLevels, elems, settings.invDivider)
	effect = getValues(settings.effColumn, settings.gradedSecLevels, elems, settings.effDivider)
	maint = getValues(settings.invColumn, settings.gradedSecLevels, elems, settings.maintDivider)

	wf.write(object(iter, abbr, fullName, invest, effect, maint))
	iter = iter + 1

wf.write(printTemplateFooter())

rf.close()
wf.close()

if settings.showskipped:
	print("")
print("Created schema with file name: ".format(settings.writeToFile))
