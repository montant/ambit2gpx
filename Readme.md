# Introduction #

Convert in gpx format a sml file transfered by moveslink application from a suunto ambit watch to a computer.

As this tool comes as an Python script, you need to have a Python interpreter available on your computer. ambit2gpx has been tested with Python 2.7 as available with ActivePython distribution, on Windows. It should run flawlessly with other interpreters/platforms.


# Details #

When transfering data with moveslink, an sml file is stored on computer. On Windows, it can be found on locations such as:

  * C:\Documents and Settings\'username'\Application Data\Suunto\Moveslink2 (on Windows XP)
  * C:\Documents and Settings\'username'\AppData\Roaming\Suunto\Moveslink2 (on Windows 7)

Pay attention to the fact these 'Application Data'/'AppData' folders are hidden by default as they are 'system folders'. Change settings of Windows explorer if you want to make them visible.

Once you have located the sml file you want to convert, Open a Command Prompt and run:
python ambit2gpx.py path\to\smlfile.sml

A file named smlfile.gpx will be created alongside the original one.

Some command line options are available, run ambit2gpx.py with no options for a description.

Enjoy. If you face any issue or would like to request some new features, you are welcome to use Issues tab of Ambit2gpx project.