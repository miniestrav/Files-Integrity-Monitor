'''
This module implements a common interface to many different
secure hash and message digest algorithms.
'''
import hashlib
'''
The OS module in Python provides functions for creating and
removing a directory (folder), fetching its contents, changing and identifying the current directory
'''
import os
'''
glob (short for global) is used to return all file paths that
match a specific pattern.
'''
import glob

import pathlib
import datetime  # Access Date/Time Information
import time

'''
for event listener to terminate running/continuous process
'''
from pynput import keyboard

'''
tkinter is a module used to create the GUI
'''
# import tkinter as tk
from tkinter import *
import tkinter.font as font
from tkinter.filedialog import askdirectory


# baselines = "%USERPROFILE%\Desktop" -- creates a path and folder called Desktop in fileIntegrity folder
'''
Baselines folder created in the user desktop
'''
baselines = pathlib.Path.home() / 'Desktop/baselines'

baseline_path = ''

files_changed = []
files_added = []
files_removed = []
files_all = []

'''
MODES:
r: open an existing file for a read operation.
w: open an existing file for a write operation. If the file already contains some data then it will be overridden but if the file is not present then it creates the file as well.
a:  open an existing file for append operation. It won’t override existing data.
 r+:  To read and write data into the file. The previous data in the file will be overridden.
w+: To write and read data. It will override existing data.
a+: To append and read data from the file. It won’t override existing data.

File Object created to store logs
'''
log_file = open("logs.txt", "a")

'''
Note: Retrieve all items found in a given path. ('.') means we are looking in the current directory

Method returns list of filenames and their hash from data (contents) in the file
A hash value is a unique value that corresponds to the content of the file. 

Rather than identifying the contents of a file by its file name, extension, or other designation, 
a hash assigns a unique value to the contents of a file.
'''
def calculate_data_hash(filename):
    # Created array to store the files within the directory
    # files = {}
    # For loop goes through each file in the directory and provides a hash value
    # for file in [item for item in os.listdir('.') if os.path.isfile(item)]:
        # CHANGE HASH TO THE FOLLOWING:
        # = hashlib.sha256()

    hash_value = hashlib.sha1()
    '''
    'rb' mode opens the file in binary format for reading
    Feeding string objects into update() is not supported, as hashes work on bytes, not on characters.
    '''
    with open(filename, 'rb') as f:
        chunk = 0
        '''
        loops till the end of the file
        '''
        while chunk != b'':
            chunk = f.read(1024)
            '''
            Update the hash object with the bytes-like object
            '''
            hash_value.update(chunk)
            '''
            hexdigest() : Returns the encoded data in hexadecimal format. In other words, returns the 
            hex representation of digest
            
            Note: This may be used to exchange the value safely in email or other non-binary environments.
            '''
            # temp = hash_value.hexdigest()
        #     files[file] = temp
        # print(files)
        return hash_value.hexdigest()

'''
Method calculates hash from name of a file
'''
def calculate_name_hash(filename):
    hash_val = hashlib.sha1()
    '''
    enoding is the act of converting information into a particular form.
    The encode() method encodes the string, using the specified encoding. 
    If no encoding is specified, UTF-8 will be used.
    
    UTF-8 is an encoding system for Unicode. It can translate any Unicode character to a 
    matching unique binary string, and can also translate the binary string back to a Unicode 
    character. This is the meaning of “UTF”, or “Unicode Transformation Format.”
    '''
    hash_val.update(filename.encode())
    '''
    hexdigest() : Returns the encoded data in hexadecimal format
    '''
    return hash_val.hexdigest()

'''
Method to update the baseline of the files within the folder selected
'''
def UpdateBaseline(dir, mode):
    if dir == "":
        message_folder_label.configure(text="Error: Folder not selected")

    elif os.path.isdir(baselines) == False:
        message_folder_label.configure(text="Baselines Folder doesn't exists, so creating it")
        os.makedirs(baselines)

        username = os.environ.get('USERNAME')
        current_datetime = datetime.datetime.now()
        string_logging = str(username) + " " + str(current_datetime)
        log_actions.set("Log: " + string_logging + "\n\tBaselines Folder Created:\n\tfor Dir: " + dir)
        print(log_actions.get())
        log_file.write("Log: " + string_logging + "\n\tBaselines Folder Created\n\tfor Dir: " + dir + '\n')

        message_folder_label.configure(text="Updating Baseline...")
        UpdateBaselineHelper(dir, mode)
        message_folder_label.configure(text="Updated Baseline Successfully")

    else:
        message_folder_label.configure(text="Updating Baseline...")

        username = os.environ.get('USERNAME')
        current_datetime = datetime.datetime.now()
        string_logging = str(username) + " " + str(current_datetime)
        log_actions.set("Log: " + string_logging + "\n\tBaseline Updated:\n\tfor Dir: " + dir)
        print(log_actions.get())
        log_file.write("Log: " + string_logging + "\n\tBaseline Updated\n\tfor Dir: " + dir + '\n')

        UpdateBaselineHelper(dir, mode)
        message_folder_label.configure(text="Updated Baseline Successfully")

'''
Method update Baseline Helper for files in a folder and files in subfolders
'''
def UpdateBaselineHelper(dir, mode):
    global name_hash, baseline_path
    '''
    At the location specified in the variable, baselines (aka baselines folder), 
    add the baseline path of each file and store them into the following variables
    '''
    if (mode == 'w'):
        name_hash = calculate_name_hash(dir)
        baseline_path = os.path.join(baselines, (name_hash + '.txt'))

        print("\tin Dir: " + baseline_path)
        log_file.write("\tin Dir: " + baseline_path + '\n')

    '''
    # Python program to demonstrate: os.path.abspath()

    # file name stored in variable file_name
    file_name = 'GFG.txt'
       
    # prints the absolute path of current
    # working directory with file name
    print(os.path.abspath(file_name))
    
    Output:
    /home/geeks/Desktop/gfg/GFG.txt
    '''

    '''
    # glob.glob gets list of all files/dirs in data folder
    # wile os.path.join() combines two or more components of a path name
    glob(os.path.join(dir, '*')) then joins the file names with the directory path you are listing.
    '''
    files = [os.path.abspath(f) for f in glob.glob(os.path.join(dir, '*')) if os.path.isfile(f)]
    '''
    Actual Creation of the individual paths and their hashes into the 'baselines' folder
    '''
    with open(baseline_path, mode) as baseline:
        for f in files:
            hash = calculate_data_hash(os.path.join(dir, f))
            baseline.write(f)
            baseline.write("=")
            baseline.write(str(hash))
            baseline.write("\n")

    '''
    This part checks for subfolders within the directory and recursively calls itself
    to obtain the hashes for the files within the subfolders
    '''
    directories = [d for d in glob.glob(os.path.join(dir, '*')) if os.path.isdir(d)]
    for d in directories:
        UpdateBaselineHelper(d, 'a')

'''
Method returns dictionary containing keys as file name and values as their hashes
Note: these are split in baselines.txt with an '=' sign

A dictionary is an abstract data type that defines an unordered collection 
of data as a set of key-value pairs. 

example: x = dict(name = "John", age = 36, country = "Norway")
'''
def getKeyHashesFromBaseline():
    global name_hash, baseline_path
    dict = {}

    with open(baseline_path, 'r') as baseline:
        for line in baseline:
            key, value = line.split('=')
            dict[key] = value[:-1]
    '''
    Example of return:
    ['C:...username\Documents\check_fileIntegrity\Account Access.txt': 'dcf18c1596c12e86f2210b8f28122918d54d19b1', 
    'C:...username\Documents\check_fileIntegrity\Account Info.txt': '85a07c998cac92113d10979c56d9cc0103aee8a8',...]
    '''
    return dict

'''
Method clears data in all 4 lists
'''
def ClearData():
    files_changed.clear()
    files_added.clear()
    files_removed.clear()
    files_all.clear()

    fm.configure(text="")
    fa.configure(text="")
    fr.configure(text="")

'''
Method configures labels to display appropriate result to user of the Integrity of the folder
With the help of CheckIntegrityHelper() Method
'''

def CheckIntegrity(dir, number):
    ClearData()  # Clear data in all 4 lists

    if dir == "":
        message_folder_label.configure(text="Error: Folder not selected")

    else:
        CheckIntegrityHelper(dir, number)
        fm.configure(text='\n'.join(files_changed))
        fa.configure(text='\n'.join(files_added))
        fr.configure(text='\n'.join(files_removed))
        # message_folder_label.configure(text="Integrity Checked Successfully")

'''
Method that checks for the integrity of the files within the folder selected by checking
the hashes in the baselines.txt file upon button click
'''
def CheckIntegrityHelper(dir, number):
    global name_hash, baseline_path

    if (number):
        name_hash = calculate_name_hash(dir)
        baseline_path = os.path.join(baselines, (name_hash + '.txt'))
        try:
            with open(baseline_path, 'r') as baseline:
                random = 99  # dummy code to handle an error
        except IOError:
            message_folder_label.configure(text='Error: Baseline file for specified folder not present')
            return

    files = [os.path.abspath(f) for f in glob.glob(os.path.join(dir, '*')) if os.path.isfile(f)]
    for x in files:
        files_all.append(x)
    dict = getKeyHashesFromBaseline()

    username = os.environ.get('USERNAME')
    current_datetime = datetime.datetime.now()
    string_logging = str(username) + " " + str(current_datetime)
    log_actions.set("Log: " + string_logging + "\n\tIntegrity Checked" + "\n\tfor Dir: " + dir)
    print(log_actions.get())
    log_file.write("Log: " + string_logging + "\n\tIntegrity Checked with the following result ->" + "\n\tfor Dir: " + dir + '\n')

    for f in files:
        # Checking for changed files
        temp_hash = calculate_data_hash(os.path.join(dir, f))
        if str(os.path.join(dir, f)) in dict.keys() and temp_hash != dict[f]:
            log_file.write('\tFiles were Modified\n')
            files_changed.append(os.path.abspath(f).replace(os.path.abspath(folder), "."))

        # Checking for added files
        if str(os.path.join(dir, f)) not in dict.keys():
            log_file.write('\tFiles were Added\n')
            files_added.append(os.path.abspath(f).replace(os.path.abspath(folder), "."))

    '''
    Again, This part checks for subfolders within the directory and recursively calls itself
    to obtain the hashes for the files within the subfolders
    '''
    directories = [d for d in glob.glob(os.path.join(dir, '*')) if os.path.isdir(d)]
    for d in directories:
        CheckIntegrityHelper(d, 0)

    if number == 1:
        # checking for removed files
        for x in list(dict.keys()):
            if x not in files_all:
                log_file.write('\tFiles were Removed\n')
                files_removed.append(os.path.abspath(x).replace(os.path.abspath(folder), "."))
    message_folder_label.configure(text="Integrity Checked Successfully")

'''
Browse button Method
'''
def open_file():
    global folder
    folder = askdirectory(parent=main_screen, title="Upload File")
    if folder:
        message_folder_label.configure(text="Folder Uploaded Successfully")
        selected_folder_label.config(text=folder)

        username = os.environ.get('USERNAME')
        current_datetime = datetime.datetime.now()
        string_logging = str(username) + " " + str(current_datetime)

        log_actions.set("Log: " + string_logging + "\n\tFolder Selected: " + folder)
        print(log_actions.get())
        log_file.write("Log: " + string_logging + "\n\tFolder Selected: " + folder + '\n')
        ClearData()

''' 
---------------- Graphical User Interface ------------------------
'''
# Create GUI window
main_screen = Tk()
# set the configuration of GUI window size
# (x,y)
main_screen.geometry("600x650")
# set window color
main_screen['background']='#232621'
# main_screen.configure(bg='black')
# set the title of GUI window
main_screen.title("Integrity Monitor: ")

'''
using environ.get() method to get current username
using datetime.datetime.now() gets current date and time
these variables must be constantly updated before the logging occurs
'''
username = os.environ.get('USERNAME')
current_datetime = datetime.datetime.now()
string_logging = str(username) + " " + str(current_datetime)

'''
Global Variable used to print to the console and log user actions
'''
global log_actions
log_actions = StringVar()
log_actions.set("Log: " + string_logging + "\n\tApplication Booted")
print(log_actions.get())
log_file.write("Log: " + string_logging + "\n\tApplication Booted" + '\n')

''' 
Styling Variables created ->
'''
# FOR BUTTONS:
brwseBtnFont = font.Font(family='Arial', size=10, weight='bold')
btnFont = font.Font(family='Arial', size=15, weight='bold')
btn_bg_clr = "#c74223"
btn_hover_clr = "#148f3f"

# FOR LABELS:
fileUpldFont = ("Arial", 10)
label_font = ("Arial", 14)
label_fg_clr = "#eac5b4"
label_bg_clr = "#232621"
error_label_clr = "#red"

folder = ""

'''
Buttons and Labels Created:
'''
changes_made_label = Label(main_screen, text="Select a folder:", wraplength=500, bg = label_bg_clr, font=label_font,fg= label_fg_clr,)
changes_made_label.place(relx=0.3, y=37, anchor='center')

browse_btn = Button(text="Click to Browse", font=brwseBtnFont,fg=label_fg_clr, height="2", width="15", bg=btn_bg_clr, command=open_file)
browse_btn.place(relx=0.7, y=40, anchor='center')

selected_folder_label = Label(main_screen, text="", wraplength=500, bg=label_bg_clr, font=label_font, fg="white",)
selected_folder_label.place(relx=0.5, y=125, anchor='center')

message_folder_label = Label(main_screen, text="", wraplength=500, bg=label_bg_clr, font=fileUpldFont, fg="green")
#message appears under click to browse button
message_folder_label.place(relx=0.7, y=80, anchor='center')

update_baseline_btn = Button(text="Update Baseline", font=btnFont, height="2", width="20", fg=label_fg_clr, bg=btn_bg_clr, command=lambda:UpdateBaseline(folder,'w'))
update_baseline_btn.place(relx=0.50, y=200, anchor='center')

check_integrity_btn = Button(text="Check File Integrity", font=btnFont, height="2", width="20", fg=label_fg_clr, bg=btn_bg_clr, command=lambda:CheckIntegrity(folder,1))
check_integrity_btn.place(relx=0.50, y=275, anchor='center')

''' -------------------------------------------- '''

fm_label = Label(main_screen, text="Files Modified:", wraplength=500, bg=label_bg_clr, font=label_font, fg=label_fg_clr)
fm_label.place(relx=0.2, y=400, anchor='center')

fm = Label(main_screen, text="", wraplength=500, bg=label_bg_clr, font=label_font, fg="white")
fm.place(relx=0.6, y=400, anchor='center')

fa_label = Label(main_screen, text="Files Added:", wraplength=500, bg=label_bg_clr, font=label_font, fg=label_fg_clr)
fa_label.place(relx=0.2, y=475, anchor='center')

fa = Label(main_screen, text="", wraplength=500, bg=label_bg_clr, font=label_font, fg="white")
fa.place(relx=0.6, y=475, anchor='center')

fr_label = Label(main_screen, text="Files Removed:", wraplength=500, bg=label_bg_clr, font=label_font, fg=label_fg_clr)
fr_label.place(relx=0.2, y=550, anchor='center')

fr = Label(main_screen, text="", wraplength=500, bg=label_bg_clr, font=label_font, fg="white")
fr.place(relx=0.6, y=550, anchor='center')

main_screen.mainloop()
'''
--------------------- END OF GUI ---------------------------
'''

''' 
Code below checks for any changes made after selecting a 
folder in the Integrity Checker Application using keyboard.Listener()
Press space key to end program

Note: This part of the program does not show changes made to files within subfolders but can detect changes
made within folders to an extent. For instance, adding or removing an item within the subfolder
will let you know that the subfolder has been modified.
'''
global stamp
global cached_stamp
global count

cached_stamp = 0
count = 0

'''
os.path.getmtime() method  is used to get the time(in seconds) of last modification 
of the specified path. 

The dict() function creates a dictionary.
'''
def files_to_timestamp(path):
    files = [os.path.join(path, f) for f in os.listdir(path)]
    return dict([(f, os.path.getmtime(f)) for f in files])

break_program = False
def on_press(key):
    global break_program
    # print(key)
    if key == keyboard.Key.space:
        print('------Program Terminated------')
        break_program = True
        return False

print("Application Closed")
username = os.environ.get('USERNAME')
current_datetime = datetime.datetime.now()
string_logging = str(username) + " " + str(current_datetime)
log_file.write("Log: " + string_logging + '\n\tApplication Closed\n')
print('------Program Started------')
print('Watching {} for changes...'.format(folder))

with keyboard.Listener(on_press=on_press) as listener:
    while break_program == False:
        '''
        folder comes from open_file() method [browsing]
        '''
        path_to_watch = folder
        print('program running...\t (press SPACE to TERMINATE) ')

        '''
        checks for subfolders
        '''
        directories = [d for d in glob.glob(os.path.join(folder, '*')) if os.path.isdir(d)]
        for d in directories:
            path_to_watch = d

        before = files_to_timestamp(path_to_watch)
        time.sleep(4)
        after = files_to_timestamp(path_to_watch)

        added = [f for f in after.keys() if not f in before.keys()]
        removed = [f for f in before.keys() if not f in after.keys()]
        modified = []

        for f in before.keys():
            if not f in removed:
                if os.path.getmtime(f) != before.get(f):
                    modified.append(f)

        if added:
            username = os.environ.get('USERNAME')
            current_datetime = datetime.datetime.now()
            string_logging = str(username) + " " + str(current_datetime)
            print('Item Added: {}'.format(', '.join(added)))
            log_file.write('Log: ' + string_logging + '\n\tItem Added: {}'.format(', '.join(added)) + '\n')
        if removed:
            username = os.environ.get('USERNAME')
            current_datetime = datetime.datetime.now()
            string_logging = str(username) + " " + str(current_datetime)
            print('Item Removed: {}'.format(', '.join(removed)))
            log_file.write('Log: ' + string_logging + '\n\tItem Removed: {}'.format(', '.join(removed)) + '\n')
        if modified:
            username = os.environ.get('USERNAME')
            current_datetime = datetime.datetime.now()
            string_logging = str(username) + " " + str(current_datetime)
            print('Item Modified: {}'.format(', '.join(modified)))
            log_file.write( 'Log: ' + string_logging + '\n\tItem Modified: {}'.format(', '.join(modified)) + '\n')
        before = after
    listener.join()