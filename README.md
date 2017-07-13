# gps-track
Android application that uses the built-in GPS receiver, written in Python 3 and based on Sl4A

# ----------------------------

Simple, lightweight and low battery usage application for Android devices. To run this application, You must install on device:

* SL4A - Scripting Layer for Android APK Download and 
* Python interpreter for Android. 


The system consists of 4 files written in Python 3:

  * katalogi.py: config file, wherein you must declare main path and path to output file (in 2 Python variables)

  * myspatial.py: file with function required to run application

  * gps-track.py: file which You must run, to save your path to simple text file (CSV format) with geometry in base WKT format (vertices with latitude and longitute)

  * csv-kml.py: file which You can run, when you can transform before saved text file to XML format file: KML (Keyhole Markup Language) and KMZ file, that You can open in Google Earth application or other GIS apps.

The application automatically removes duplicate coordinate points (don't save it), what is very helpfull for import data to Trailforks database or other restricted spatial database system.
