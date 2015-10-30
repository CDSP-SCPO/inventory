#!/usr/bin/python
# -*- coding: utf-8 -*-
# Execution example : python daneelolivaw.py path/to/the/scanning/sheet.csv path/to/the/METS/file.xml

#
# Libs
#
import codecs, csv, json, logging, operator, os, sys

#
# Config
#
path_separator = '/'
log_folder = 'log'
log_level = logging.DEBUG
results_folder = 'results'
# data_folder = 'data'
# data_file = 'type_documents.csv'
csv_separator = '\t'
csv_data = ''
json_data = []
recordsbyid = {}
id = 0

#
# Programm
#
def main(recordsbyid) :
	global csv_data
	global json_data
	log_file = log_folder + path_separator + sys.argv[0].replace('.py', '.log')
	logging.basicConfig(filename = log_file, filemode = 'w', format = '%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = log_level)
	logging.info('Start')
	# If specified, open the quality control sheet to list the documents
	logging.info('Open quality control sheet')
	# Load scanning sheet if any
	if has_scanning_sheet :
		with open(control_sheet, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			t = [l for l in spamreader]
			recordsbyid = dict(zip(map(operator.itemgetter(0), t), t))
	# Start inventory on the main folder
	inventory(inventory_path, recordsbyid)
	# Write the results into data files
	writeCsvFile(csv_data)
	writeJsonFile(json_data)
	logging.info('End')
	print 'Everything worked well !\nCSV and JSON files have been generated into \'' + results_folder + '\' folder.'

def inventory(path, recordsbyid) :
	global id
	global csv_data
	global json_data
	# Iterate over each folder and file from path
	for file in os.listdir(path) :
		complete_path = os.path.join(path, file)
		# If it is a file
		if os.path.isfile(complete_path) :
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
				if has_scanning_sheet :
					# Check if the file was listed in the quality control sheet
					try :
						file_data = recordsbyid['_'.join(splitted_file[:9]).split('.')[0]]
						file_article_title = file_data[9]
						file_view_number = file_data[15]
						file_date = file_data[10]
					except KeyError :
						logging.info('Key error : the file ' + path + path_separator + file + ' doesn\'t exist in the quality control sheet.')
				csv_data += csv_separator.join(['%04d' % (id), path, file, collection, subcollection, folder, subfolder, lang, subject, article, rank, extension]) + '\n'
				# Check that this folder already exists or create it
				if len(list((item for item in json_data if item['name'] == file.split('_')[3]))) == 0 :
					json_data.append({'name' : file.split('_')[3], 'type' : 'folder', 'values' : []})
				tmp = (item for item in json_data if item['name'] == file.split('_')[3]).next()
				# Check that this folder already exists or create it
				if len(list((item for item in tmp['values'] if item['name'] == file.split('_')[4]))) == 0 :
					tmp['values'].append({'name' : file.split('_')[4], 'type' : 'folder', 'values' : []})
				tmp = (item for item in tmp['values'] if item['name'] == file.split('_')[4]).next()
				# Check that this folder already exists or create it
				if len(list((item for item in tmp['values'] if item['name'] == file.split('_')[5]))) == 0 :
					tmp['values'].append({'name' : file.split('_')[5], 'type' : 'folder', 'values' : []})
				tmp = (item for item in tmp['values'] if item['name'] == file.split('_')[5]).next()
				# Finally add this file
				tmp['values'].append({'file' : file, 'date' : file_date, 'article_title' : file_article_title, 'view_number' : file_view_number, 'serie_number' : rank})
			# Else write a log
			else :
				logging.error('File not conforme : ' + path + file)
		# If it is a folder, launch inventory on it
		else :
			inventory(complete_path, recordsbyid)

def writeCsvFile(data) :
	# Add csv headers
	csv_headers = ['N° d\'inventaire', 'Chemin', 'Fichier', 'Fonds', 'Sous-fonds', 'Dossier', 'Sous-dossier', 'Langue', 'Sujet', 'Article', 'N° (série)', 'Extension']
	data = csv_separator.join(csv_headers) + data
	# Write results into a csv data file
	csv_file = results_folder + path_separator + sys.argv[0].replace('.py', '.csv')
	with codecs.open(csv_file, 'w', 'utf8') as f:
		f.write(data.decode('utf8'))
	f.close()

def writeJsonFile(data) :
	# Write results into an json data file
	json_file = results_folder + path_separator + sys.argv[0].replace('.py', '.json')
	with open(json_file, 'w') as f:
		json.dump(data, f, indent = 4, separators = (',', ': '), encoding = "utf-8", ensure_ascii = False)

#
# Main
#
if __name__ == '__main__':
	# Check that the command line has at least one argument
	if len(sys.argv) < 2 :
		print 'Arguments error'
		print 'Correct usage : ' + sys.argv[0] + ' "path/to/folder/to/inventory" "path/to/the/quality/control/sheet.csv"'
		print 'The second argument ie. the digitalization sheet is optional and has to be a csv file'
	else :
		# Check that if the command line has a second argument, it is a csv file
		if len(sys.argv) >= 3 and sys.argv[2][-4:] != '.csv' :
			print 'The second argument ie. the quality control sheet has to be a CSV file'
		# Check that if the command line has a third argument, it is an xml file
		if len(sys.argv) >= 4 and sys.argv[3][-4:] != '.xml' :
			print 'The third argument ie. the METS file has to be an XML file'
		else :
			inventory_path = sys.argv[1]
			if len(sys.argv) >= 3 :
				has_scanning_sheet = 1
				control_sheet = sys.argv[2]
			else :
				has_scanning_sheet = 0
			# Check that log folder exists, else create it
			if not os.path.exists(log_folder):
				os.makedirs(log_folder)
			# Check that results folder exists, else create it
			if not os.path.exists(results_folder):
				os.makedirs(results_folder)
			main(recordsbyid)