#!/usr/bin/python
# -*- coding: utf-8 -*-
# Execution example : python inventory.py "path/to/folder/to/inventory" "survey_name" "path/to/the/quality/control/sheet.csv"

#
# Libs
#
import codecs, csv, json, logging, operator, os, re, sys

#
# Config
#
path_separator = '/'
log_folder = 'log'
log_level = logging.DEBUG
results_folder = 'results'
data_folder = 'data'
data_file = data_folder + path_separator + 'type_documents.json'
file_name = 'classification_tree'
csv_separator = '\t'
recordsbyid = {}
blacklist_extension = ['jp2', 'txt']
current_folder = ''
# List of the folder to inventory according to the format of the result file
data = {
	'csv' : {'pre' : '', 'col' : '', 'anal' : '', 'ana' : '', 'add' : ''},
	'json' : {'pre' : [], 'col' : [], 'anal' : [], 'ana' : [], 'add' : []},
	'txt' : {'pre' : '', 'col' : '', 'anal' : '', 'ana' : '', 'add' : ''}
}
id = 0

#
# Function
#
# Create a numerical sort
def numericalSort(value):
	numbers = re.compile(r'(\d+)')
	parts = numbers.split(value)
	parts[1::2] = map(int, parts[1::2])
	return parts

#
# Programm
#
def main(recordsbyid) :
	global data
	log_file = log_folder + path_separator + sys.argv[0].replace('.py', '.log')
	logging.basicConfig(filename = log_file, filemode = 'w', format = '%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = log_level)
	logging.info('Start')
	# If specified, open the quality control sheet to list the documents
	logging.info('Open quality control sheet')
	recordsbyid = {}
	# Load quality control sheet if any
	if has_quality_control_sheet :
		with open(quality_control_sheet, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
			for x in spamreader :
				if len(x) == 21 :
					recordsbyid[x[1]] = x
	# Start inventory on the main folder
	inventory(inventory_path, recordsbyid)
	# Write the results into data files
	writeCsvFile(data)
	writeJsonFile(data)
	writeTxtFile(data)
	logging.info('End')
	print ''
	print 'Everything worked well !\nJSON and TXT files have been generated into \'' + results_folder + '\' folder.\nCSV file has been generated into the inventoried folder.'

def inventory(path, recordsbyid) :
	global id
	global data
	global current_folder
	# Iterate over each folder and file from path
	for file in sorted(os.listdir(path), key = numericalSort) :
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
				file_data = ''
				file_article_title = ''
				file_view_number = ''
				file_date = ''
				if has_quality_control_sheet :
					# Check if the file was listed in the quality control sheet
					try :
						file_data = recordsbyid['_'.join(splitted_file[:9]).split('.')[0]]
						file_article_title = file_data[10]
						file_view_number = file_data[16]
						file_date = file_data[11]
					except KeyError :
						logging.info('Key error : the file ' + path + path_separator + file + ' doesn\'t exist in the quality control sheet.')
				if not extension in blacklist_extension :
					data['csv'][current_folder] += csv_separator.join(['%04d' % (id), path, file, collection, subcollection, folder, subfolder, lang, subject, article, rank, extension, '', '']) + '\n'
					# Check that subcollection already exists or create it
					if len(list((item for item in data['json'][current_folder] if item['name'] == subcollection))) == 0 :
						label = getTranslation(subcollection, merged_dict)
						data['json'][current_folder].append({'name' : subcollection.encode('utf8'), 'type' : 'folder', 'values' : [], 'label' : label.encode('utf8')})
						data['txt'][current_folder] += '. ' + label.encode('utf8') + ' [' + subcollection + ']\n'
					tmp = (item for item in data['json'][current_folder] if item['name'] == subcollection).next()
					# Check that this folder already exists or create it
					if len(list((item for item in tmp['values'] if item['name'] == folder))) == 0 :
						label = getTranslation(folder, merged_dict)
						tmp['values'].append({'name' : folder.encode('utf8'), 'type' : 'folder', 'values' : [], 'label' : label.encode('utf8')})
						data['txt'][current_folder] += '\t' + str(len(tmp['values'])) + '. ' + label.encode('utf8') + ' [' + folder + ']\n'
					tmp = (item for item in tmp['values'] if item['name'] == folder).next()
					# Check that this folder already exists or create it
					if len(list((item for item in tmp['values'] if item['name'] == subfolder))) == 0 :
						label = getTranslation(subfolder, merged_dict)
						tmp['values'].append({'name' : subfolder, 'type' : 'folder', 'values' : [], 'label' : label.encode('utf8')})
						data['txt'][current_folder] += '\t\t' + str(len(tmp['values'])) + '. ' + label.encode('utf8') + ' [' + subfolder + ']\n'
					tmp = (item for item in tmp['values'] if item['name'] == subfolder).next()
					# Finally add this file to the classification tree
					tmp['values'].append({'file' : file, 'date' : file_date, 'article_title' : file_article_title, 'view_number' : file_view_number, 'serie_number' : rank, 'type' : 'file'})
					if not '_transcr_' in file :
						data['txt'][current_folder] += '\t\t\t'
						if file_article_title != '' :
							data['txt'][current_folder] += file_article_title
						if file_date != '' :
							data['txt'][current_folder] += ' (' + file_date + ')'
						if rank != '' :
							data['txt'][current_folder] += ' ' + rank
						data['txt'][current_folder] += '\n\t\t\t\t' + file + '\n'
					elif '_transcr_' in file and extension == 'pdf' :
						if file_article_title != '' :
							data['txt'][current_folder] += '\t\t\t' + file_article_title
						if file_date != '' :
							data['txt'][current_folder] += ' (' + file_date + ')'
						if rank != '' :
							data['txt'][current_folder] += ' ' + rank
						data['txt'][current_folder] += '\n\t\t\t\t' + file + ' (Et versions .xml et .odt)' + '\n'
			# Else write a log
			else :
				logging.error('File not conforme : ' + path + path_separator + file)
		# If it is a folder, launch inventory on it
		else :
			if file in data['csv'].keys() :
				current_folder = file
			inventory(complete_path, recordsbyid)

def writeCsvFile(data) :
	# Add csv headers
	csv_headers = ['N° d\'inventaire', 'Chemin', 'Fichier', 'Fonds', 'Sous-fonds', 'Dossier', 'Sous-dossier', 'Langue', 'Sujet', 'Article', 'N° (série)', 'Extension', 'download', 'online']
	data = csv_separator.join(csv_headers) + '\n' + data['csv']['pre'] + data['csv']['col'] + data['csv']['anal'] + data['csv']['ana'] + data['csv']['add']
	# Check that CSV folder exists, else create it
	csv_folder = inventory_path + path_separator + 'add'
	if not os.path.exists(csv_folder) :
		os.makedirs(csv_folder)
	csv_file = csv_folder + path_separator + file_name + '.csv'
	# Write results into a CSV data file
	with codecs.open(csv_file, 'w', 'utf8') as f:
		f.write(data.decode('utf8'))
	f.close()

def writeJsonFile(data) :
	# Write results into a JSON data file
	json_file = results_folder + path_separator + file_name + '.json'
	with open(json_file, 'w') as f:
		json_data = data['json']['pre'] + data['json']['col'] + data['json']['anal'] + data['json']['ana'] + data['json']['add']
		json.dump(json_data, f, indent = 4, separators = (',', ': '), encoding = "utf-8", ensure_ascii = False)
	f.close()

def writeTxtFile(data) :
	# Write results into a TXT data file
	txt_file = results_folder + path_separator + file_name + '.txt'
	counter = 0
	with codecs.open(txt_file, 'w', 'utf8') as f:
		if data['txt']['pre'] != '' :
			counter += 1
			f.write(str(counter) + data['txt']['pre'].decode('utf8'))
		if data['txt']['col'] != '' :
			counter += 1
			f.write(str(counter) + data['txt']['col'].decode('utf8'))
		if data['txt']['anal'] != '' :
			counter += 1
			f.write(str(counter) + data['txt']['anal'].decode('utf8'))
		if data['txt']['ana'] != '' :
			counter += 1
			f.write(str(counter) + data['txt']['ana'].decode('utf8'))
		if data['txt']['add'] != '' :
			counter += 1
			f.write(str(counter) + data['txt']['add'].decode('utf8'))
	f.close()

def getTranslation(item, dictionnary) :
	if item in dictionnary.keys() :
		label = dictionnary[item]
	else :
		label = ''
		logging.warning('There is no label for : ' + item + ' in this dictionnary.')
	return label

#
# Main
#
if __name__ == '__main__':
	# Check that the command line has at least 3 arguments
	if len(sys.argv) < 3 or (len(sys.argv) >= 4 and sys.argv[3][-4:] != '.csv') :
		print ''
		print 'Arguments error'
		print 'Correct usage : python ' + sys.argv[0] + ' "path/to/folder/to/inventory" "survey_name" "path/to/the/quality/control/sheet.csv"'
		print 'The first argument ie. the path to inventory is mandatory and is the path to the folder to inventory'
		print 'The second argument ie. the name of the survey is mandatory and is used to match with the dedicated dictionary'
		print 'The third argument ie. the quality control sheet is optional and has to be a CSV file'
	else :
		# Dynamically get the project name to load the linked dictionary
		inventory_path = sys.argv[1]
		inventory_path_splitted = inventory_path.split(path_separator)
		inventory_folder = inventory_path_splitted[-1] if inventory_path_splitted[-1] != '' else inventory_path_splitted[-2]
		survey_name = sys.argv[2]
		if len(sys.argv) >= 4 :
			has_quality_control_sheet = 1
			quality_control_sheet = sys.argv[3]
		else :
			has_quality_control_sheet = 0
		# Check that log folder exists, else create it
		if not os.path.exists(log_folder) :
			os.makedirs(log_folder)
		# Check that results folder exists, else create it
		if not os.path.exists(results_folder) :
			os.makedirs(results_folder)
		# Read the type_documents dictionnary
		type_documents = json.load(open(data_file))
		my_data_file = data_folder + path_separator + 'type_documents_' + survey_name + '.json'
		# TODO : Check if file exists
		my_type_documents = json.load(open(my_data_file))
		merged_dict = {key: value for (key, value) in (type_documents.items() + my_type_documents.items())}
		main(recordsbyid)