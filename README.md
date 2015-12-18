# inventory


## Former name

daneelolivaw


## What for ?

Inventory a folder with formatted files' names and generate a classification tree.

JP2 and TXT files are not inventoried (blacklist_extension array).


## How to use it ?

Inventory can be used with any system compatible with python 2.7 by invoking the command

`python inventory.py "path/to/folder/to/inventory" "survey_name" "path/to/the/quality/control/sheet.csv"`

 * The first argument ie. the path to inventory is mandatory and is the path to the folder to inventory
 * The second argument ie. the name of the survey is mandatory and is used to match with the dedicated dictionary
 * The third argument ie. the quality control sheet is optional and has to be a CSV file


## What is the output ?

The ouput is a classification tree based on the files' name. The tree format will be JSON, CSV and TXT.

The JSON and TXT files are in the 'results' folder.

The CSV file is in the inventoried folder, in the 'add' folder.


## Credits

[Sciences Po - CDSP](http://cdsp.sciences-po.fr/)