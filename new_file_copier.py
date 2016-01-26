from tkinter import *
import shutil, os, time, sqlite3
import datetime
from datetime import date
from stat import *

global now, timestamp, conn, minute, lastUpdate

# connect to database 'updates.db'
conn = sqlite3.connect('updates.db')

# create the "updates_info" table if it doesn't already exist
conn.execute("CREATE TABLE IF NOT EXISTS updates_info(ID INTEGER PRIMARY KEY AUTOINCREMENT, TIMESTAMP TEXT);")

# Retrieve the last update from the database
cursor = conn.execute("SELECT MAX(ID), TIMESTAMP from updates_info")
s = str(cursor.fetchall())
lastUpdate =  s[5:21]

# Function to get the path of the directory to read from
def getReadPath():
    global src
    src = filedialog.askdirectory()
    
# Function to get the path of the directory to copy new files to
def getWritePath():
    global dst
    dst = filedialog.askdirectory()

# Function to copy all files that have been created or updated in the last 24 hours
def move(*args):
    listofFiles = os.listdir(src)
    for i, f in enumerate(listofFiles):
        st = os.stat(src+"/"+listofFiles[i])
        if st[ST_MTIME] > (time.time() - 86400):
            fullPath = src + "/" + f
            shutil.copyfile(fullPath, dst + "/" + f)
            
    # Dialog box to alert user that function completed sucessfully
    messagebox.showinfo("Success", "All files created or modified in the last 24 hours have been copied to " + dst)

    # Generate a timestamp for current database update
    now = datetime.datetime.now()
    if now.minute < 10:
        minute = '0' + str(now.minute)
    else:
        minute = str(now.minute)
    timestamp = str(now.month) + "/" +str(now.day) + "/" + str(now.year) + " " + str(now.hour) + ":" + minute

    # Update database with the newest timestamp
    conn.execute("INSERT INTO updates_info (TIMESTAMP) VALUES ('" + timestamp + "')");
    conn.commit()
                     
    
# Function to make the main window of the GUI and place buttons and label within it
def makeWindow():
    win = Tk()
    b1 = Button(win, text = "Choose Read Folder", command=getReadPath)
    b2 = Button(win, text = "Choose Write Folder", command=getWritePath)

    b1.grid(row = 0, column = 0, padx = 5, pady = 5)
    b2.grid(row = 0, column = 1, padx = 5, pady = 5)
    
    label = Label(win, text = "Last Update: " + lastUpdate)
    b3 = Button(win, text = "Copy New Files", command=move)

    label.grid(row = 2, columnspan = 2, column = 0, padx = 5, pady = 5)
    b3.grid(row = 3, columnspan = 2, column = 0, padx = 5, pady = 5)
    
    return win

# Loop for the GUI
win = makeWindow()
win.title("File Mover")
win.mainloop()
