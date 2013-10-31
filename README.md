CoCoViLaSchemaGenerator
=======================

Script to generate .syn files from .csv format for graded security level optimization in CoCoViLa 

 * *[CoCoViLa repository](http://sourceforge.net/projects/cocovila/)*
 * *[CoCoViLa homepage](http://www.cs.ioc.ee/cocovila/)*


Tested on LibreOffice Calc Version 4.0.2.2 and Python 2.7.4

Reads input from CSV file with specific format described below:

Investment levels are calculated for example: 5600/1000 = 5.6
Dividing by 1000 is done by the script

Positions in csv:

1.  Abbreviation
2.  Full name
3.  First level investment
4.  Second level investment
5.  Third level investment
6.  Forth level investment
7.  First level effectiveness
8.  Second level effectiveness
9.  Third level effectiveness
10.  Forth level effectiveness

Maintainability is calculated from the investment level. Default is 1/5 of investment.
