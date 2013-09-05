CoCoViLaSchemaGenerator
=======================

Script to generate .syn files for CoCoViLa from .csv format

Tested on LibreOffice Calc Version 4.0.2.2 and Python 2.7.4

Reads input from CSV file with specific input.
Investment levels are calculated for example: 5600/1000 = 5.6
Dividing by 1000 is done by the script

Positions in csv:
1) Abbrevation
2) Full name

3) First level investment
4) Second level investment
5) Third level investment
6) Forth level investment

7) First level effectivness
8) Second level effectivness
9) Third level effectivness
10) Forth level effectivness

Maintainability is calculated from the investment level. Default is 1/5 of investment.
