from contextlib import nullcontext
import os
import shutil
import sys
from datetime import date
import tkinter as tk
from tkinter import DISABLED, filedialog, Text
from turtle import title


#DFiles 0: Source Path    1: Drop Path   2: Video Path
DFiles = []
root = tk.Tk()
root.title('Drop Off Lane')



#Save info between executions function
def LogInfo(SPath, VPath, DPath) :
    with open('DropFile.txt', 'w') as f:
        f.write(SPath + "," + VPath + "," + DPath + "," + LFV + ",")

def fixVideo() :
    if len(DFiles) < 3 :
        DFiles.append("null")
    sortFiles(DFiles[0], DFiles[2], DFiles[1])

#Sort Function
def sortFiles(SPath, VPath, DPath) :

    for widgets in frame.winfo_children():
      widgets.destroy()

    if VPath == "null" :
        VPath = SPath

    #ERROR check dir
    if os.path.exists(SPath) == False:
        for widgets in frame.winfo_children():
            input("**ERROR** Press Enter to continue")
            sys.exit("Directory Does Not Exist")

    #creates a list, loads the directory on the sd card for PHOTOS, populates the list with the file paths for all photos
    locPhotos = []

    for file in os.listdir(SPath):
        if file.endswith(".ARW"):
        
            locPhotos.append(os.path.join(SPath, file))

          
    #print('*' + str(len(locPhotos)) + ' Photos Found*') 
    print("Photos")
    print(len(locPhotos))


    if os.path.exists(VPath) : 
        #get videos
        locVideos = []

        for file in os.listdir(VPath):
            if file.endswith(".MP4"):
            
                locVideos.append(os.path.join(VPath, file))
        
    #print('*' + str(len(locVideos)) + ' Videos Found*')
    print("Videos")
    print(len(locVideos))


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
            os.chdir(DPath + '/' + fDate)
    #if the file doesnt exist create one
    if exists == False :
        os.mkdir(fDate)
        print(fDate + " was created")
        os.chdir(DPath + '/' + fDate)

    #creates a video folder
    if os.path.exists(os.getcwd() + '/Video') == False :
        os.mkdir('Video')

    #move the photos
    os.chdir(DPath + '/' + fDate)
    i = 0
    for str in locPhotos :
        shutil.move(locPhotos[i], os.getcwd())
        i += 1

    #move the videos
    os.chdir(DPath + '/' + fDate + '/Video')
    y = 0
    for str in locVideos :
        shutil.move(locVideos[y], os.getcwd())
        y += 1

    #pause to read text outs
    input("Press Enter to continue...")
    quit()
    






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
    #tkinter frame
    frame = tk.LabelFrame(root, bg="#fcfbd2", padx=10, pady=10)

    explain = tk.Label(frame, text="Enter the location. Then click the buttons on the left to confirm the location").grid(row=0, column=1)

    #3 buttons for the different paths
    e1 = tk.Entry(frame, width=50)
    e1.grid(row=1, column=1)

    e2 = tk.Entry(frame, width=50)
    e2.grid(row=2, column=1)

    e3 = tk.Entry(frame, width=50)
    e3.grid(row=3, column=1)
    
    #3 buttons to lock in paths
    Button1 = tk.Button(frame, text="Photo Path", padx=20, command=lambda: DFiles.insert(0, e1.get())).grid(row=1, column=0)
    Button2 = tk.Button(frame, text="Video Path", padx=21, command=lambda: DFiles.insert(2, e2.get())).grid(row=2, column=0)
    Button3 = tk.Button(frame, text="Drop Path", padx=23, command=lambda: DFiles.insert(1, e3.get())).grid(row=3, column=0)

    #button starts the main part of the program [sortFiles]
    Button4 = tk.Button(frame, text="Continue", padx=25, command=lambda: fixVideo())
    Button4.grid(row=4, column=0)
    
    frame.pack()

root.mainloop()