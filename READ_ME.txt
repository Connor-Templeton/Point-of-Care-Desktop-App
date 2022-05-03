Read me for code breakdown of the 2022 UMN spring senior design team desktop python GUI

DESCRIPTION:
This code creates a python GUI for running the handheld deivce. It created a file called Test_Set when opened.
This stores the CSV text files it creates when the Run Test button is pressed. The Rename button renames the CSV file
and changes the corresponding text box. The delete button deletes the CSV file and writes over the test line in the 
GUI. The plot button brings up another window with a plot of the data, voltage vs time.



IMPORTS and FILES:
The libraries used were tkinter, serial, numpy, matplotlib, csv, os, and time.
It references an image file called icon.png for the created windows icon.

VARIABLES:
test_list array is used to create the buttons in a given test row.
test_num indicates what row the test is in. This serves to identify the tests and place them.

MAIN WINDOW SETUP:
Sets the window size to 600x500 and background color to marroon. The title and icon are also defined here.



FUNCTIONS:

def add_test():
	This function creates a new test row and increments test_num. The buttons created and title of the test
	use the test_num variable to indentify what row they are. The m= in the Button lines is the passing of the
	row identifier to the function the button calls.

def delete_test(which_test):
	This function uses the test_num passed to it as which_test to delete specfic files in the Test_Set folder
	that is created on start up of the GUI. It also overlays a text box with deleted to let the user know that
	that test has been deleted.

def ReadData(which_test):
	This function uses the test_num passed to it as which_test to write to a file called test"insert number of
	test here".txt after the code write to the device bb and reads back BB. The code then sends cc to start the
	data reading and saving.

def rename(which_test):
	This function uses the test_num passed to it as which_test to rename that tests cvs file. A dialof option
	pops up to ask the new name of the file which the code then renames it to. The GUI is also updates with
	the same format used in add_test() but using which_test to get a previous row.

def plot(which_test):
	This function uses the test_num passed to it as which_test to save to the the file './Test_Set/test'+ 
	which_test + '.txt' The function reads out the data by character and converts it to voltage. Once all the data
	is read out the function writes to the data file to add the time.

	Then the function plots the data as the list area. This plot is in a new window.

START-UP:
This code creates the intial test_set text box and folder as well as the add_test button. The device connection text
box indicates with "device connected!" if the serial port send aa then reads back AA.

The auto determination of port-ID has code for Vinit's computers and Connor's. Reading out the port information
of the computer and adding it to the elif statements is necessary for new machines.
