#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Todo
#
# Add "numéro d'inventaire" column and data
# Add "Date" min and max column and data
# Date format : AAAA-MM-JJ or AAAA-MM or AAAA
# Add an HTML / text format output

#
# Libs
#
import codecs, csv, logging, operator, os

#
# Config
#
rootPath = "/Users/anne.lhote/Documents/beQuali/meta_documents/cdsp_bq_sp5/sp5-ol"
pathSeparator = "/"
logFolder = 'log'
logFile = logFolder + pathSeparator + 'daneelolivaw.log'
logLevel = logging.DEBUG
dataFolder = 'data'
dataOutput = dataFolder + pathSeparator + 'daneelolivaw.csv'
outputSeparator = '\t'
data = 'chemin' + outputSeparator + 'fichier' + outputSeparator + 'fonds' + outputSeparator + 'sous-fonds' + outputSeparator + 'dossier' + outputSeparator + 'sous-dossier' + outputSeparator + 'langue' + outputSeparator + 'sujet' + outputSeparator + 'article' + outputSeparator + 'n° (série)' + outputSeparator + 'extension' + '\n'
controlSheet = '/Users/anne.lhote/www/beQuali/meta_documents/data/bordereau_controle_qualite_lot01_michelat.csv'
recordsbyid = {}

#
# Programm
#
logging.basicConfig(filename = logFile, filemode = 'w', format = '%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = logLevel)
logging.info('Start')

def main() :
	global data
	global recordsbyid
	logging.info('Read control sheet')
	with open(controlSheet, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		# UTF-8 pb
		t = [l for l in spamreader]
		recordsbyid = dict(zip(map(operator.itemgetter(0), t), t))
	inventory(rootPath)
	writeFile(data)
	logging.info('End')

def inventory(path) :
	global data
	global recordsbyid
	for file in os.listdir(path) :
		completePath = os.path.join(path, file)
		if os.path.isfile(completePath) :
			if len(file.split('_')) >= 9 :
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
				try :
					print recordsbyid['_'.join(file.split('_')[:9]).split('.')[0]]
				except KeyError :
					logging.info('Key error : the file ' + file + ' doesn\'t exist in the control sheet.')
				data += path + outputSeparator + file + outputSeparator + collection + outputSeparator + subcollection + outputSeparator + folder + outputSeparator + subfolder + outputSeparator + lang + outputSeparator + subject + outputSeparator + article + outputSeparator + rank + outputSeparator + extension + '\n'
			else :
				logging.error('File not conforme : ' + path + file)
		else :
			inventory(completePath)

def writeFile(data) :
	# Write result into file
	with codecs.open(dataOutput, 'w', 'utf8') as f:
		f.write(data.decode('utf8'))
	f.close()

#
# Main
#
if __name__ == '__main__':
	main()