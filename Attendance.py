import tkinter
from tkinter import *
from PIL import ImageTk, Image
from tkinter import PhotoImage
from tkinter import messagebox
import threading
import datetime
import numpy as np
import csv
import cv2
import os
import time
import faceRecognition as fr
from tkinter import filedialog
from PIL import ImageTk, Image
#import face_recognition
from datetime import datetime
import pandas as pd
from pandas import DataFrame, Series




root=Tk()
root.title("Attendence System")
root.geometry("1000x600+150+0")
root.config(bg="#FFFFFF")
root.resizable(False, False)



#---------------------------------------------------------------------VIEW ATTENDANCE CODE----------------------------------------------------#
def view_csv(read_csv):
    read_csv.delete('0.0', END)
    with open('Attendance_Users.csv', 'r+') as f:
        myDataList = f.readlines()
        IDList=[]
        nameList = []
        visitDate = []
        visitTime = []
        for line in myDataList:
            entry = line.split(',')
            print(entry)
            IDList.append(entry[0])
            nameList.append(entry[1])
            visitDate.append(entry[2])
            visitTime.append(entry[3])
        for i in range(len(nameList)):
            read_csv.insert(END, "\t - (" + str(i) + ") |  " + IDList[i] + " \t\t | " + str(nameList[i]) + " \t\t | " + str(visitDate[i]) +" \t\t | " + str(visitTime[i]) +"\n")
            read_csv.insert(END, "\t....................................................................................................................................")
            read_csv.insert(END, "\n")
#---------------VIEW ATTENDANCE WINDOW--------------
def viewAttendanceWindow():
    viewWindow = Tk()
    viewWindow.title("View Attendence")
    viewWindow.geometry("1000x600+150+0")
    viewWindow.config(bg="#FFFFFF")
    viewWindow.resizable(False, False)
    # VIEEW ATTENDANCE LABEL HERE
    viewAttHeading = Label(viewWindow, text='Student Attendance Details',
                           font=("times new roman", 30, "bold"), bg="#FFFFFF", fg='#65A2E8',padx=20,pady=10)
    viewAttHeading.pack(fill=X,)
    # # QUIT BUTTON
    quit_btn = Button(viewWindow, compound=LEFT,  text="<<  Back",font=("times new roman", 13, "bold"),bg="#65A2E8", fg="#191919", activebackground="#191919", activeforeground="#65A2E8", cursor="hand2",command=viewWindow.destroy)
    quit_btn.place(x=50, y=80, relwidth=0.1)

    # creating a window in WINDOW 1 for showing reg.csv file
    viewWindowFrame1=LabelFrame(viewWindow ,relief=FLAT, font=("times new roman", 18), fg ="white", bg="#262626", bd=3)
    viewWindowFrame1.place(x=50,y=120,relwidth=0.9,height='450')
    # reading .csv file to see how many user have been registered
    scroll_y = Scrollbar(viewWindowFrame1, width=20)
    scroll_y.pack(side=RIGHT, fill=Y)
    read_csv = Text(viewWindowFrame1, font=('times new roman', 15),bg="#262626",fg ="white", yscrollcommand=scroll_y.set)
    read_csv.place(x=0, y=0, relwidth=0.98, relheight=1)
    scroll_y.config(command=read_csv.yview)
    # # view btn to view registered users
    view_btn = Button(viewWindow, text="Update Attendance", font=("times new roman", 13, "bold"),bg="#65A2E8", fg="#191919", activebackground="#191919", activeforeground="#65A2E8", cursor="hand2", command=view_csv(read_csv))
    view_btn.place(x=700, y=80, relwidth=0.25)



#------------------------------------------------------------REGISTERED USER CODE----------------------------------------------------------------------#
def Reg_user_window():
    wlcm_scrn = tkinter.Toplevel()
    wlcm_scrn.title('Registration')
    wlcm_scrn.geometry("1000x600+150+0")
    wlcm_scrn.resizable(False, False)
    wlcm_scrn.config(bg='skyblue')

    # Title
    title = Label(wlcm_scrn, text="ATTENDANCE SYSTEM", font=("times new roman", 30), bg="#262626", fg="lightblue", pady=10, bd=5,relief=GROOVE)
    title.pack(fill=X)
    # Back Button
    quit_btn = Button(wlcm_scrn, compound=LEFT, text="<<  Back", font=("times new roman", 13, "bold"), bg="#65A2E8", fg="#191919", activebackground="#191919", activeforeground="#65A2E8", cursor="hand2", command=wlcm_scrn.destroy)
    quit_btn.place(x=50, y=500, relwidth=0.1)

    # Sub Window for registration
    Window1 = Frame(wlcm_scrn, bg="snow2", bd=10, relief=RIDGE)
    Window1.place(x=230, y=110, height=450, width=550)

    # add student logo icon
    '''icon = Image.open("Images/student.jpg")

    icon = icon.resize((150, 120))
    img = ImageTk.PhotoImage(icon)
    label = Label(Window1, image=img)
    label.place(x=193.5, y=10)
    # icon= ImageTk.PhotoImage(file="student.png")
    # lbl_image=Label(root,image=icon)
    # lbl_image.place(x=300,y=50)'''

    reg_img = Image.open("Images/student.jpg")
    my_resized = reg_img.resize((150, 150), Image.ANTIALIAS)

    resized_reg = ImageTk.PhotoImage(my_resized)
    lbl_reg_image = Label(Window1, image=resized_reg, compound=LEFT)
    lbl_reg_image.place(x=193.5, y=10)



    Label0 = Label(Window1, text=" STUDENT REGISTRATION ", font=("ariel", 18, "bold"), bg="DeepSkyBlue3", fg="black")
    Label0.place(x=58, y=160, width=420)


    # enter id label
    Label0 = Label(Window1, text="Enter ID No ", font=("times new roman", 16, "bold"), bg="snow2", fg="black")
    Label0.place(x=110, y=240)

    id_entry = Entry(Window1,  font=("times new roman", 14), bg="gray97", fg="black")
    id_entry.place(x=250, y=240, width=190)


    #enter name label
    Label1 = Label(Window1, text="Enter Name  ", font=("times new roman", 16, "bold"), bg="snow2", fg="black")
    Label1.place(x=110, y=280)

    # box for taking name as user input

    name_entry = Entry(Window1, font=("times new roman", 14), bg="gray97", fg="black")
    name_entry.place(x=250, y=280, width=190)

    def reg_user():

        my_name = name_entry.get()
        id = id_entry.get()

        # id cant be a string check condition
        try:
            int(id)
        except Exception:
            my_result = " ERROR: Please enter a NUMERIC value"
            messagebox.showerror("Error", "ERROR: Please enter a NUMERIC value")
            print(" Only numeric values allowed ")
            return

        # id already exist
        my_csv = pd.read_csv('Registered_Users.csv')
        list_id = my_csv[my_csv['ID'] == int(id)].index.tolist()
        if len(list_id) > 0:
            my_result = " ERROR: ID already exist "
            messagebox.showerror("Error", "ERROR: ID already exist")
            print(" ERROR: ID already exist ")
            return

        # conditions verified now camera is turned on

        cap = cv2.VideoCapture(0)
        org_path = os.getcwd()
        print(org_path)

        with open('Registered_Users.csv', 'r+') as f:
            myDataList = f.readlines()
            # print(type(myDataList))
            # print(myDataList)
            nameList = []

            '''id = 0
            for line in myDataList:
                id = id + 1
                entry = line.split(',')
                nameList.append(entry[0])'''
            if my_name not in nameList:
                now = datetime.now()
                dt_date = now.strftime("%d/%m/%Y")
                dt_time = now.strftime('%H:%M:%S')
                f.writelines(f'{id},{my_name},{dt_date} ,{dt_time} \n')
                print(id)

        count = 0
        while count<100:
            ret, test_img = cap.read()
            if not ret:
                continue
            dirpath = os.path.join(r"E:/5th Semester/VP Practicals/VP-Project-main/trainingImages", str(id))
            try:
                os.mkdir(dirpath)
            except FileExistsError:
                x = 5
                # print('Directory {} already exists'.format(dirpath))
            else:
                print('Directory {} created'.format(dirpath))

            os.chdir(dirpath)
            cv2.imwrite("./frame%d.jpg" % count, test_img)  # save frame as JPG file
            count += 1
            resized_img = cv2.resize(test_img, (1000, 700))
            cv2.imshow('face detection Tutorial ', resized_img)
            key = cv2.waitKey(10)
            if key == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

        os.chdir(org_path)
        print(os.getcwd())

        faces, faceID = fr.labels_for_training_data('trainingImages')
        face_recognizer = fr.train_classifier(faces, faceID)
        face_recognizer.write('Registered_Users.yml')
        
        
        messagebox.showinfo("Registration", "Student has successfully registered!")
    # Registration button
    Reg_btn = Button(Window1, text="REGISTER", command=reg_user)
    Reg_btn.place(x=198, y=355, width=150, height=60)


    wlcm_scrn.mainloop()

#my_result=" WELCOME "
# User Registartion Function



#------------------------------------------------------------DETECT USER CODE----------------------------------------------------------------------#
def Det_user_window():
    #Defining root windows
    root=Tk()
    root.title("Attendence System")
    root.geometry("1000x600+150+0")
    root.config(bg="#FFFFFF")
    root.resizable(False, False)

    #Defining label for the header
    l1 = Label(root, text="DETECTING STUDENT", font=("times new roman", 30, "bold"), bg="#262626", fg ="lightblue", pady=10, bd=5, relief=GROOVE)
    l1.pack(fill=X)



    """#Defining windows for the camera feed
    vidWindow = LabelFrame(root, bg="lightblue")
    vidWindow.place(x=0, y=100, relwidth=1, relheight=0.9)
    """

    #Button for detection
    btn1 = Button(root, text="Start Detection", command=detect_user, font=("times new roman", 14, "normal"), bg="#65A2E8", fg="black", pady=5, bd=None)
    btn1.place(x=10, y=100)

    #Label for some info
    lbl1 = Label(root, text="Press Esc to exit Video Streaming", font=("time new roman", 16, "bold"), fg="#65A2E8", bg="white")
    lbl1.place(x=350, y=150)

    #Button for Quit detection
    btn2 = Button(root, text="Quit Detection", command=root.destroy, font=("times new roman", 14, "normal"), bg="#65A2E8", fg="black", pady=5, bd=None)
    btn2.place(x=850, y=100)

    root.mainloop()
    return root

def detect_user():
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read('Registered_Users.yml')  # Load saved training data

    cap = cv2.VideoCapture(0)

    while True:
        ret, test_img = cap.read()  # captures frame and returns boolean value and captured image
        faces_detected, gray_img = fr.faceDetection(test_img)

        # cv2.imshow('face detection Tutorial ',resized_img)
        # cv2.waitKey(10)

        f = open('Registered_Users.csv', 'r')
        reader = csv.reader(f)
        name = {}
        next(reader, None)
        for row in reader:
            name[row[0]] = row[1]

        for face in faces_detected:
            (x, y, w, h) = face
            roi_gray = gray_img[y:y + w, x:x + h]
            label, confidence = face_recognizer.predict(roi_gray)  # predicting the label of given image
            print("confidence:", confidence)
            print("label:", label)
            fr.draw_rect(test_img, face)
            str_lbl = str(label)
            predicted_name = name[str_lbl]
            if confidence < 39:
                # If confidence less than 37 then don't print predicted face text on screen
                    fr.put_text(test_img, predicted_name, x, y)
                    with open('Attendance_Users.csv', 'r+') as f:
                        myDataList = f.readlines()
                        nameList = []
                        id=0
                        for line in myDataList:
                            id = id + 1
                            entry = line.split(',')
                            nameList.append(entry[0])
                            print(nameList)
                        if str_lbl not in nameList:
                            now = datetime.now()
                            dt_date = now.strftime("%d/%m/%Y")
                            dt_time = now.strftime('%H:%M:%S')
                            f.writelines(f'{str_lbl},{predicted_name},{dt_date} ,{dt_time} \n')



        resized_img = cv2.resize(test_img, (800, 600))
        cv2.imshow('Detecting Students', resized_img)
        key = cv2.waitKey(10)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()




# -----------MAIN WINDOW---------------

bg_img=Image.open("Images/customized.png")
resized=bg_img.resize((1000,600), Image.ANTIALIAS)

resized_bg=ImageTk.PhotoImage(resized)
lbl_image=Label(root,image=resized_bg, compound=LEFT)
lbl_image.place(x=0, y=0)



reg_user=Button(root,text="REGISTER STUDENT",command=Reg_user_window, font=("times new roman", 15, "bold"), bg="#65A2E8", fg="#191919", activebackground="#191919", activeforeground="#65A2E8", cursor="hand2")
reg_user.place(x=60,y=340,width=300,height=40)


atnd_user=Button(root,text="LIVE ATTENDENCE",command=Det_user_window, font=("times new roman", 15, "bold"), bg="#65A2E8", fg="#191919", activebackground="#191919", activeforeground="#65A2E8", cursor="hand2")
atnd_user.place(x=60,y=410,width=300,height=40)


atnd_user=Button(root,text="VIEW ATTENDANCE", font=("times new roman", 15, "bold"), bg="#65A2E8", fg="#191919", activebackground="#191919", activeforeground="#65A2E8", cursor="hand2" , command=viewAttendanceWindow)
atnd_user.place(x=60,y=480,width=300,height=40)
root.mainloop()
