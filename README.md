# inventory


## Former name

daneelolivaw


## What for ?

Inventory a folder with formatted files' names and generate a classification tree.

.jp2 and .txt files are not inventoried.


## How to use it ?

Inventory can be used with any system compatible with python 2.7 by invoking the command

`python inventory.py "path/to/folder/to/inventory" "path/to/the/quality/control/sheet.csv"`


## What is the output ?

The ouput is a classification tree based on the files' name. The tree format will be JSON, CSV and TXT.

The JSON and TXT files are in the 'results' folder.

The CSV file is in the inventoried folder, in the 'add' folder.


## Credits

[Sciences Po - CDSP](http://cdsp.sciences-po.fr/)