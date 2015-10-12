#!/usr/bin/python
# -*- coding: utf-8 -*-
# Execution example : python daneelolivaw.py /path/to/folder/to/inventory /path/to/the/quality/control/sheet.csv

#
# Todo
#
# Add an HTML / text format output
# Add Git Readme file
# Comments

#
# Libs
#
import codecs, csv, logging, operator, os, sys

#
# Config
#
pathSeparator = '/'
logFolder = 'log'
logFile = logFolder + pathSeparator + 'daneelolivaw.log'
logLevel = logging.DEBUG
dataFolder = 'data'
dataOutput = dataFolder + pathSeparator + 'daneelolivaw.csv'
outputSeparator = '\t'
data = 'N° d\'inventaire' + outputSeparator + 'Chemin' + outputSeparator + 'Fichier' + outputSeparator + 'Fonds' + outputSeparator + 'Sous-fonds' + outputSeparator + 'Dossier' + outputSeparator + 'Sous-dossier' + outputSeparator + 'Langue' + outputSeparator + 'Sujet' + outputSeparator + 'Article' + outputSeparator + 'N° (série)' + outputSeparator + 'Extension' + '\n'
recordsbyid = {}
id = 0

#
# Programm
#
def main(recordsbyid) :
	global data
	logging.basicConfig(filename = logFile, filemode = 'w', format = '%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = logLevel)
	logging.info('Start')
	logging.info('Open quality control sheet')
	if hasControlSheet :
		with open(controlSheet, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			t = [l for l in spamreader]
			recordsbyid = dict(zip(map(operator.itemgetter(0), t), t))
	# Start inventory on the main folder
	inventory(inventoryPath, recordsbyid)
	writeFile(data)
	logging.info('End')

def inventory(path, recordsbyid) :
	global id
	global data
	for file in os.listdir(path) :
		completePath = os.path.join(path, file)
		if os.path.isfile(completePath) :
			if len(file.split('_')) >= 9 :
				id += 1
				collection = '_'.join(file.split('_')[0:3])
				subcollection = file.split('_')[3]
				folder = file.split('_')[4]
				subfolder = file.split('_')[5]
				lang = file.split('_')[6]
				subject = file.split('_')[7]
				article = '_'.join(file.split('_')[8:]).split('.')[0].split('_')[0]
				if len('_'.join(file.split('_')[8:]).split('.')[0].split('_')) == 2 :
					rank = '_'.join(file.split('_')[8:]).split('.')[0].split('_')[1]
				else :
					rank = ''
				extension = file.split('.')[-1]
				if hasControlSheet :
					# Check if the file was listed in the quality control sheet
					try :
						recordsbyid['_'.join(file.split('_')[:9]).split('.')[0]]
					except KeyError :
						logging.info('Key error : the file ' + path + pathSeparator + file + ' doesn\'t exist in the quality control sheet.')
				data += "%04d" % (id) + outputSeparator + path + outputSeparator + file + outputSeparator + collection + outputSeparator + subcollection + outputSeparator + folder + outputSeparator + subfolder + outputSeparator + lang + outputSeparator + subject + outputSeparator + article + outputSeparator + rank + outputSeparator + extension + '\n'
			else :
				logging.error('File not conforme : ' + path + file)
		else :
			inventory(completePath, recordsbyid)

def writeFile(data) :
	# Write result into file
	with codecs.open(dataOutput, 'w', 'utf8') as f:
		f.write(data.decode('utf8'))
	f.close()

#
# Main
#
if __name__ == '__main__':
	# Check that the command line has at least one argument
	if len(sys.argv) < 2 :
		print 'Arguments error'
		print 'Correct usage : ' + sys.argv[0] + ' "/path/to/folder/to/inventory" "/path/to/the/quality/control/sheet.csv"'
		print 'The quality control sheet is optional and has to be a csv file'
	else :
		# Check that if the command line has a second argument, it is a csv file
		if len(sys.argv) >= 3 and sys.argv[2][-4:] != '.csv' :
			print 'The second argument ie. the quality control sheet has to be a csv file'
		else :
			inventoryPath = sys.argv[1]
			if len(sys.argv) >= 3 :
				hasControlSheet = 1
				controlSheet = sys.argv[2]
			else :
				hasControlSheet = 0
			# Check that log folder exists, else create it
			if not os.path.exists(logFolder):
				os.makedirs(logFolder)
			# Check that data folder exists, else create it
			if not os.path.exists(dataFolder):
				os.makedirs(dataFolder)
			main(recordsbyid)