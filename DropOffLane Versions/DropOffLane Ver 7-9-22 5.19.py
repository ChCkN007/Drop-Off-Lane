from contextlib import nullcontext
import os
import shutil
import sys
from datetime import date
import tkinter as tk
from tkinter import filedialog, Text

print('************ Loading Files ************')

root = tk.Tk()
frame = tk.LabelFrame(root, text="Select Paths", bg="#fcfbd2", padx=10, pady=10)

#DFiles 0: Source Path    1: Video Path   2: Drop Path   3: video?
DFiles = []

def EntryTransfer(data1, data2, data3) :
    DFiles.insert(0, data1.get())
    DFiles.insert(1, data2.get())
    DFiles.insert(2, data3.get())
    frame.destroy



isEnd = False
#tkinter canvas code
#canvas = tk.Canvas(root, height=500, width=500, bg="#fcfbd2").pack()

#function to get all needed data if it doesn't already exist
def NoFileRoute() :

    label1 = tk.Label(frame, text="Source Path").grid(row=0, column=0)
    label2 = tk.Label(frame, text="Video Path").grid(row=1, column=0)
    label3 = tk.Label(frame, text="Dro Path").grid(row=2, column=0)

    e1 = tk.Entry(frame, width=50)
    e1.grid(row=0, column=1)

    e2 = tk.Entry(frame, width=50)
    e2.grid(row=1, column=1)

    e3 = tk.Entry(frame, width=50)
    e3.grid(row=2, column=1)


    Button4 = tk.Button(frame, text="Continue", padx=25, pady=5, command=EntryTransfer(e1, e2, e3))
    Button4.grid(row=3, column=0)
    
    frame.pack()
    



#Save info between executions function
def LogInfo(SPath, VPath, DPath, LFV) :
    with open('DropFile.txt', 'w') as f:
        f.write(SPath + "," + VPath + "," + DPath + "," + LFV + ",")



#Sort Function
def sortFiles(SPath, VPath, DPath) :
    #ERROR check dir
    if os.path.exists(SPath) == False:
        input("**ERROR** Press Enter to continue")
        sys.exit("Directory Does Not Exist")

    #creates a list, loads the directory on the sd card for PHOTOS, populates the list with the file paths for all photos
    locPhotos = []

    for file in os.listdir(SPath):
        if file.endswith(".ARW"):
        
            locPhotos.append(os.path.join(SPath, file))
    print('*' + str(len(locPhotos)) + ' Photos Found*')


    #ERROR check dir
    if os.path.exists(VPath) == False:
        input("**ERROR** Press Enter to continue")
        sys.exit("Directory Does Not Exist")

    #get videos
    locVideos = []

    for file in os.listdir(VPath):
        if file.endswith(".MP4"):
        
            locVideos.append(os.path.join(VPath, file))
    print('*' + str(len(locVideos)) + ' Videos Found*')


    #load photo dir on pc, check if folder exists for current date, add photos to file

    #date
    today = date.today()
    fDate = today.strftime("%m-%d-%y")


    #ERROR check dir
    if os.path.exists(DPath) == False:
        input("**ERROR** Press Enter to continue")
        sys.exit("Directory Does Not Exist")

    #changes dir
    os.chdir(DPath)

    #checks if the date already has a file   !!!Make better with os.path.exists()!!!!!
    exists = False
    for file in os.listdir():
        if file == fDate :
            exists = True
            print(fDate + " already exists")
            os.chdir(DPath + fDate)
    #if the file doesnt exist create one
    if exists == False :
        os.mkdir(fDate)
        print(fDate + " was created")
        os.chdir(DPath + fDate)

    #creates a video folder
    if os.path.exists(os.getcwd() + '/Video') == False :
        os.mkdir('Video')

    #move the photos
    os.chdir(DPath + fDate)
    i = 0
    for str in locPhotos :
        shutil.move(locPhotos[i], os.getcwd())
        i += 1

    #move the videos
    os.chdir(DPath + fDate + '/Video')
    y = 0
    for str in locVideos :
        shutil.move(locVideos[y], os.getcwd())
        y += 1

    #pause to read text outs
    input("Press Enter to continue...")
    






#MAIN LOGIC

#Loads save file if it exists
if os.path.isfile('DropFile.txt'):
    with open('DropFile.txt', 'r') as f:
        tempFiles = f.read()
        tempFiles = tempFiles.split(',')
        DFiles = [x for x in tempFiles if x.strip()]
    print('        Program Initialized         ')




#gathers info if the save doesnt exist to write later
if os.path.exists("DropFile.txt") == False or os.stat("DropFile.txt").st_size == 0 : 
    NoFileRoute()
    


#sortFiles(SourcePath, VideoPath, DropPath)

#LogInfo(SourcePath, VideoPath, DropPath, LookForVideo)

root.mainloop()