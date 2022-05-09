#written by Connor Templeton 4/21/22

from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilename
from turtle import bgcolor
import csv
import os
import os.path
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import serial
import time
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

rows, cols = (50, 50)
test_list = [[0]*cols]*rows
test_num = [0]*50
test_num[0] = 2
i=0
#had to define g for Arturo's auto detection
g=None




#MAIN WINDOW SETUP

# the main Tkinter window
window = Tk()

# setting the title
window.title('MPS Research Environment')

# dimensions of the main window
window.geometry("600x500")

# Color of Window
window.configure(bg="#800000")

# Creating object of photoimage class
# Image should be in the same folder
# in which script is saved
p1 = PhotoImage(file = 'icon.png')

# Setting icon of master window
window.iconphoto(False, p1)



#FUNCTIONS TO BE CALLED BY BUTTONS AND SUCH

def add_test():
    global test_num, test_list, i
    #adding multiple buttons and text boxes
    test_list[test_num[i]][0] = Button(master = window, bg = "#FFD700", command = lambda m=str(test_num[i]-1): plot(m), height = 1, width = 5, text = "Plot")
    test_list[test_num[i]][1] = Button(window, bg = "#FFD700", text = 'Rename', command = lambda m=str(test_num[i]-1): rename(m))
    test_list[test_num[i]][2] = Button(window, bg = "#FFD700", text = 'Run Test', command = lambda m=str(test_num[i]-1): ReadData(m))
    test_list[test_num[i]][3] = Text(window, height = 1, width = 30, font= ('Redux 12'))
    test_list[test_num[i]][4] = Button(window, bg = "#FFD700", text = 'Delete', command = lambda m=str(test_num[i]-1): delete_test(m))
    test_list[test_num[i]][0].grid(row=test_num[i], column=3, sticky='nsew')
    test_list[test_num[i]][1].grid(row=test_num[i], column=4, sticky='nsew')
    test_list[test_num[i]][2].grid(row=test_num[i], column=2, sticky='nsew')
    test_list[test_num[i]][3].grid(row=test_num[i], column=1, sticky='nsew')
    test_list[test_num[i]][3].insert('end', 'test '+str(test_num[i]-1))
    test_list[test_num[i]][4].grid(row=test_num[i], column=5, sticky='nsew')
    test_num[i+1]=test_num[i]+1
    i += 1

# This is not implemented as the additon of other groups creates problems with the grid
# formatting. It will override the labels. Using Classes and keeping track of how many tests
# each group has could solve this
# def add_group():
#     new= Toplevel(window)
#     new.geometry("600x500")
#     new.title("Test Set")
#     # Color of Window
#     new.configure(bg="#800000")
#     p1 = PhotoImage(file = 'icon.png')   

#     #test title text box
#     T= Text(new, height = 1, width = 30, font= ('Redux 14 bold'))
#     T.grid(row=1, column=1)
#     T.insert('end', "Test Set1")
#     if not os.path.exists('./Test_Set'):
#         os.mkdir('./Test_Set')

#     #new test button
#     button3 = Button(new, bg = "#FFD700", text = 'Add Test', command = lambda : add_test())
#     button3.grid(row=1,column=2, pady=5)

#     #new test group button
#     button3 = Button(new, bg = "#FFD700", text = 'Add Test group', command = lambda : add_group())
#     button3.grid(row=0,column=2, pady=5)

def delete_test(which_test):
    file='./'+folder_name +'/test'+ which_test + '.txt'
    if os.path.exists(file):
        os.remove(file)
        test_list[int(which_test)+1][3].delete('1.0', END)
        test_list[int(which_test)+1][3].insert('insert', 'DELETED')
    else:
        messagebox.showerror("File Error", "Error: File does not exist")

def ReadData(which_test):

    serialport.write(b'bb')
    file='./'+folder_name +'/test'+ which_test + '.txt'
    if(serialport.read(1).hex() != "BB"):
        serialport.write(b'cc')
    with open(file, 'w') as datafile:
        datafile.write(serialport.read(510000).hex())


def rename(which_test):
    new_name = simpledialog.askstring('Rename', 'New file name (other functions do not work when file renamed)')
    filename = './' +folder_name +'/' +new_name
    file='./'+folder_name +'/test'+ which_test + '.txt'
    os.rename(file, filename)
    test_list[int(which_test)+1][3].delete('1.0', END)
    test_list[int(which_test)+1][3].insert('insert', new_name)

#Plot Data, look at current python code to see the matplotlib use case there
def plot(which_test):
    test_file='./'+folder_name +'/test'+ which_test + '.txt'
    file = open(test_file, 'r')
    list = []
    a = []
    cycle = 0
    while 1:

        char = file.read(1)          # read by character
        if not char: break
        if cycle == 6:
            cycle = 0
            a = a.replace('\n','')
            b = int(a, 16)
            c = (b/16777215)*4.096
            list.append(c)

        if cycle == 0:
            a = char

        else:
            a += char

        cycle += 1

    b = int(a, 16)
    c = (b/16777215)*4.096
    list.append(c)
    file.close()

    with open(test_file, mode='w', newline='') as magicoil_output:
        magicoil_writer = csv.writer(magicoil_output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        time = 0.0000000000000000

        for x in list:
            magicoil_writer.writerow([time, x])
            time = (time + 0.00000406504)
    magicoil_output.close()




    #Plot window creation
    new= Toplevel(window)
    new.geometry("500x500")
    new.title("Plot for Test")
    # Color of Window
    new.configure(bg="#800000")

    # Creating object of photoimage class
    # Image should be in the same folder
    # in which script is saved
    p1 = PhotoImage(file = 'icon.png')

    # Setting icon of master window
    new.iconphoto(False, p1)

	# the figure that will contain the plot
    fig = Figure(figsize = (5, 5),
				dpi = 100)
    fig.supxlabel("Time")
    fig.supylabel("Voltage")

	# adding the subplot
    plot1 = fig.add_subplot(111)

	# plotting the graph
    plot1.plot(list)
    
	# creating the Tkinter canvas
	# containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
							master = new)
    canvas.draw()

	# placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(row=8, column=4)

	# creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
								new)
    toolbar.update()

	# placing the toolbar on the Tkinter window
    canvas.get_tk_widget().grid(row=0, column=0)




#START-UP PROCEDURE, BUTTONS AND TEXT
folder_name = simpledialog.askstring('Folder Creation', 'Please name a folder for the tests')
#test title text box
T= Text(window, height = 1, width = 30, font= ('Redux 14 bold'))
T.grid(row=1, column=1)
T.insert('end', folder_name)
if not os.path.exists('./'+folder_name):
    os.mkdir('./'+folder_name)

#device conncection text box
check = Text(window, height = 1, width = 20)
check.grid(row=0, column=1)

#new test button
button3 = Button(window, bg = "#FFD700", text = 'Add Test', command = lambda : add_test())
button3.grid(row=1,column=2, pady=5)

#new test group button
# button3 = Button(window, bg = "#FFD700", text = 'Add Test group', command = lambda : add_group())
# button3.grid(row=0,column=2, pady=5)

#Auto determination of the device port-ID
# for port, desc, hwid in sorted(ports):
#     #these two if and elisf are for Vinit's Mac
#     if (port.startswith('/dev/cu.usbmodem') == True):
#         print("{}: {} [{}]".format(port, desc, hwid))
#         g = port
#     elif (port.startswith('/dev/cu.usbserial-FT') == True):
#         print("{}: {} [{}]".format(port, desc, hwid))
#         g = port
#     #this elif is for Connor's Window PC
#     elif (hwid.find('USB VID:PID=0403:6001 SER=FT4PZUI0A') != -1):
#         print("{}: {} [{}]".format(port, desc, hwid))
#         g = port

# serialport = serial.Serial(g, 115200, timeout=60)
# serialport.write(b'aa')
# if(serialport.read(1).hex() != "AA"):
#     check.insert('end', "Device Connected!")
# else:
#     check.insert('end', "Device Not Connected :(")
check.insert('end', "Device Connected!")






# run the gui
window.mainloop()