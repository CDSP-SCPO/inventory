#!/usr/bin/python
# -*- coding: utf-8 -*-
# Execution example : python daneelolivaw.py path/to/folder/to/inventory path/to/the/quality/control/sheet.csv

#
# Libs
#
import codecs, csv, logging, operator, os, sys

#
# Config
#
path_separator = '/'
log_folder = 'log'
log_file = log_folder + path_separator + 'daneelolivaw.log'
log_level = logging.DEBUG
results_folder = 'results'
csv_file = results_folder + path_separator + 'daneelolivaw.csv'
csv_separator = '\t'
csv_data = ''
html_data = ''
recordsbyid = {}
id = 0

#
# Programm
#
def main(recordsbyid) :
	global csv_data
	logging.basicConfig(filename = log_file, filemode = 'w', format = '%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = log_level)
	logging.info('Start')
	# If specified, open the quality control sheet to list the documents
	logging.info('Open quality control sheet')
	if hasControlSheet :
		with open(controlSheet, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			t = [l for l in spamreader]
			recordsbyid = dict(zip(map(operator.itemgetter(0), t), t))
	# Start inventory on the main folder
	inventory(inventoryPath, recordsbyid)
	# Write the results into data files
	writeCsvFile(csv_data)
	# TODO replace it
	html_data = 'LALILOU'
	writeHtmlFile(html_data)
	logging.info('End')

def inventory(path, recordsbyid) :
	global id
	global csv_data
	# Iterate over each folder and file from path
	for file in os.listdir(path) :
		completePath = os.path.join(path, file)
		# If it is a file
		if os.path.isfile(completePath) :
			# Check that the file name is correct
			if len(file.split('_')) >= 9 :
				# Increment the identifier in the inventory
				id += 1
				# File name pattern : collection01_collection02_collection03_subcollection_folder_subfolder_lang_subject_article_rank.extension
				splitted_file = file.split('_')
				collection = '_'.join(splitted_file[0:3])
				subcollection = splitted_file[3]
				folder = splitted_file[4]
				subfolder = splitted_file[5]
				lang = splitted_file[6]
				subject = splitted_file[7]
				article = '_'.join(splitted_file[8:]).split('.')[0].split('_')[0]
				if len('_'.join(splitted_file[8:]).split('.')[0].split('_')) == 2 :
					rank = '_'.join(splitted_file[8:]).split('.')[0].split('_')[1]
				else :
					rank = ''
				extension = file.split('.')[-1]
				if hasControlSheet :
					# Check if the file was listed in the quality control sheet
					try :
						recordsbyid['_'.join(splitted_file[:9]).split('.')[0]]
					except KeyError :
						logging.info('Key error : the file ' + path + path_separator + file + ' doesn\'t exist in the quality control sheet.')
				# csv_data += "%04d" % (id) + csv_separator + path + csv_separator + file + csv_separator + collection + csv_separator + subcollection + csv_separator + folder + csv_separator + subfolder + csv_separator + lang + csv_separator + subject + csv_separator + article + csv_separator + rank + csv_separator + extension + '\n'
				csv_data += csv_separator.join(['%04d' % (id), path, file, collection, subcollection, folder, subfolder, lang, subject, article, rank, extension])
			# Else write a log
			else :
				logging.error('File not conforme : ' + path + file)
		# If it is a folder, launch inventory on it
		else :
			inventory(completePath, recordsbyid)

def writeCsvFile(data) :
	# Add csv headers
	csv_headers = ['N° d\'inventaire', 'Chemin', 'Fichier', 'Fonds', 'Sous-fonds', 'Dossier', 'Sous-dossier', 'Langue', 'Sujet', 'Article', 'N° (série)', 'Extension']
	data = csv_separator.join(csv_headers) + data
	# Write results into a csv data file
	with codecs.open(csv_file, 'w', 'utf8') as f:
		f.write(data.decode('utf8'))
	f.close()

def writeHtmlFile(data) :
	# Write results into an html data file
	prefix = '<html><body>'
	suffix = '</body></html>'
	data = prefix + data + suffix
	print data
	# f = open('workfile', 'w')
	# f.write(data)
	# f.close()

#
# Main
#
if __name__ == '__main__':
	# Check that the command line has at least one argument
	if len(sys.argv) < 2 :
		print 'Arguments error'
		print 'Correct usage : ' + sys.argv[0] + ' "path/to/folder/to/inventory" "path/to/the/quality/control/sheet.csv"'
		print 'The second argument ie. the quality control sheet is optional and has to be a csv file'
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
			if not os.path.exists(log_folder):
				os.makedirs(log_folder)
			# Check that data folder exists, else create it
			if not os.path.exists(results_folder):
				os.makedirs(results_folder)
			main(recordsbyid)