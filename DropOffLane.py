from contextlib import nullcontext
import os
import shutil
import sys
from datetime import date
import tkinter as tk
from tkinter import filedialog, Text
from turtle import title

programPath = os.getcwd()

photoPath = ""
videoPath = ""
dropPath = ""

photoFormat = ".ARW"
videoFormat = ".MP4"

DFiles = []
root = tk.Tk()
root.title('Drop Off Lane')

frame = tk.LabelFrame(root, bg="#fcfbd2", padx=10, pady=10)


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
        if file.endswith(photoFormat):
        
            locPhotos.append(os.path.join(SPath, file))

          
    #print('*' + str(len(locPhotos)) + ' Photos Found*') 
    print("Photos")
    print(len(locPhotos))

    locVideos = []

    if os.path.exists(VPath) : 
        #get videos
        for file in os.listdir(VPath):
            if file.endswith(videoFormat):
            
                locVideos.append(os.path.join(VPath, file))
    else :
        global videoPath
        videoPath = '_'
        for file in os.listdir(SPath):
            if file.endswith(videoFormat):
            
                locVideos.append(os.path.join(SPath, file))
        
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

    #logs save data
    os.chdir(programPath)
    with open('DropFile.txt', 'w') as f:
            f.write(photoPath + ",")
            f.write(videoPath + ",")
            f.write(dropPath + ",")
            f.write(photoFormat + ",")
            f.write(videoFormat + ",")

    quit()
    
def settings() :
    global photoPath
    global videoPath
    global dropPath
    global frame

    for widgets in frame.winfo_children():
        widgets.destroy()


    explain = tk.Label(frame, text="Enter the location. Then click the buttons on the left to confirm the location").grid(row=0, column=1)

    #3 buttons for the different paths
    e1 = tk.Entry(frame, width=50)
    e1.insert(0, photoPath)
    e1.grid(row=1, column=1)

    e2 = tk.Entry(frame, width=50)
    e2.insert(0, videoPath)
    e2.grid(row=2, column=1)

    e3 = tk.Entry(frame, width=50)
    e3.insert(0, dropPath)
    e3.grid(row=3, column=1)
    
    #3 buttons to lock in paths
    Button1 = tk.Button(frame, text="Photo Path", padx=20, command=lambda: setVar(1, e1.get())).grid(row=1, column=0)
    Button2 = tk.Button(frame, text="Video Path", padx=21, command=lambda: setVar(2, e2.get())).grid(row=2, column=0)
    Button3 = tk.Button(frame, text="Drop Path", padx=23, command=lambda: setVar(3, e3.get())).grid(row=3, column=0)

    #button starts the main part of the program [sortFiles]
    Button4 = tk.Button(frame, text="Main Menu", padx=19, command=lambda: mainMenu())
    Button4.grid(row=4, column=0)

def mainMenu() :
    os.chdir(programPath)
    with open('DropFile.txt', 'w') as f:
            f.write(photoPath + ",")
            f.write(videoPath + ",")
            f.write(dropPath + ",")
            f.write(photoFormat + ",")
            f.write(videoFormat + ",")

    global frame

    for widgets in frame.winfo_children():
        widgets.destroy()

    explain = tk.Label(frame, text="Sort Files with current settings, or change them").grid(row=0, column=0)
    
    #3 buttons to lock in paths
    Button1 = tk.Button(frame, text="Sort Files", padx=20, command=lambda: sortFiles(photoPath, videoPath, dropPath)).grid(row=1, column=0)
    Button2 = tk.Button(frame, text="Settings", padx=23, command=lambda: settings()).grid(row=2, column=0)

    frame.pack()


def setVar(var, value) :
    if var == 1 :
        global photoPath
        photoPath = value
    elif var == 2:
        global videoPath
        videoPath = value
    elif var == 3:
        global dropPath
        dropPath = value

#MAIN LOGIC

#Loads save file if it exists
if os.path.isfile('DropFile.txt'):
    #make a frame
    #frame2 = tk.LabelFrame(root, bg="#fcfbde", padx=10, pady=10)

    with open('DropFile.txt', 'r') as f:
        tempData = f.read()
        tempData = tempData.split(',')
        DFiles = [x for x in tempData if x.strip()]
    
    photoPath = DFiles[0]
    videoPath = DFiles[1]
    dropPath = DFiles[2]
    photoFormat = DFiles[3]
    videoFormat = DFiles[4]
    

    explain = tk.Label(frame, text="Sort Files with current settings, or change them").grid(row=0, column=0)
    
    #3 buttons to lock in paths
    Button1 = tk.Button(frame, text="Sort Files", padx=20, command=lambda: sortFiles(photoPath, videoPath, dropPath)).grid(row=1, column=0)
    Button2 = tk.Button(frame, text="Settings", padx=23, command=lambda: settings()).grid(row=2, column=0)
    
    frame.pack()





#gathers info if the save doesnt exist to write later
if os.path.exists("DropFile.txt") == False or os.stat("DropFile.txt").st_size == 0 : 
    #tkinter frame

    explain = tk.Label(frame, text="Enter the location. Then click the buttons on the left to confirm the location").grid(row=0, column=1)

    #3 buttons for the different paths
    e1 = tk.Entry(frame, width=50)
    e1.grid(row=1, column=1)

    e2 = tk.Entry(frame, width=50)
    e2.grid(row=2, column=1)

    e3 = tk.Entry(frame, width=50)
    e3.grid(row=3, column=1)
    
    #3 buttons to lock in paths
    Button1 = tk.Button(frame, text="Photo Path", padx=20, command=lambda: setVar(1, e1.get())).grid(row=1, column=0)
    Button2 = tk.Button(frame, text="Video Path", padx=21, command=lambda: setVar(2, e2.get())).grid(row=2, column=0)
    Button3 = tk.Button(frame, text="Drop Path", padx=23, command=lambda: setVar(3, e3.get())).grid(row=3, column=0)

    #button starts the main part of the program [sortFiles]
    Button4 = tk.Button(frame, text="Continue", padx=25, command=lambda: mainMenu())
    Button4.grid(row=4, column=0)
    
    frame.pack()

root.mainloop()