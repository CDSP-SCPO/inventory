# Daneelolivaw

Inventory and check quality tool

Daneelolivaw can be used to inventory a folder with formatted files' names

It can also be used to check the presence of all the files asked to the service provider by passing the quality control sheet as second argument


## How to use it ?

Daneelolivaw can be used with any system compatible with python 2.7 by invoking the command

The second argument ie. the quality control sheet is optional and has to be a csv file

`python daneelolivaw.py path/to/folder/to/inventory path/to/the/quality/control/sheet.csv`


## When to use it ?

There are 2 way to use it in the beQuali project.

If the documents are nativaly numeric, use it to inventory the content of a folder passed as first argument.

If the documents are not natively numeric, use it as control quality on the return of the service provider. The first argument passed will be the folder sent by the service profider, the second one will be the scanning sheet and the third one the METS file return by the service provider.


## Credits

[Sciences Po - CDSP](http://cdsp.sciences-po.fr/)