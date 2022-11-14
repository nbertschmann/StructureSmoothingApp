# Structure Smoothing User Interface

I. Name
--------
Structure Smoothing User Interface

II. Purpose
------------
The purpose of this tool is to smooth out the robot grid structure to alleviate robot operation issues due to large 
changes in grid height from square to square.

III. Description
----------------
This tool recreates the surface of the grid structure using IMU data (pitch/roll) gathered by bots. This recreated 
surface is then run through a low-pass filter to ‘smooth’ it out. 
Based on these results, a delta height value is assigned to each post of the structure. The post heights should be 
manually modified based the delta value to smooth out the structure and ensure more reliable robot operation. 

IV. File list
-------------
* StructureSmoothingApp.py:      Base UI file
* CombineTilts.py:               Averages pitch and roll values from a given square, based on if using basement or 
                                 attic data
* CombineTilts2.py:              Averages pitch and roll values from a given square
* ParseLogs.py:                  Parses the log data to extract DM, X location, Y location, Z location, Pitch, Roll, 
                                 and Bot ID values
* FormatData.py:                 Formats the pitch (x_tilt) and roll (y_tilt) data into arrays
* NormalizeTilts.py:             Normalizes the pitch and roll values (tilt values) based on BotID to eliminate 
                                 variations in IMU measurements from robot to robot
* RecreateStructure.py:          Uses the pitch (Xtilt_real) and roll (Ytilt_real) values for each square to recreate 
                                 the relative heights of each post on the structure                              
* PlotArray.py:                  Generates a 3D plot of the recreated structure values
* ShowQT.py:                     Takes in the generated plotly figure and generates an html value for it to be 
                                 properly displayed
* WriteToCSV:                    Writes data values to a csv file
* README.txt: 	                 This file

V. Documentation
------------------
Full documentation available upon request

VI. Technologies
-----------------
Project was created with
* PyCharm 2021.2
* Python 3.6
* PyQt5

VI. Dependencies
-----------------
* PyQt5
* Numpy
* Pandas
* Plotly
* QWebEngine
