from user import User
import tkinter
from tkinter import *
from tkinter import Tk, Button, filedialog, Label
from functools import partial
from tkinter import messagebox 
from PIL import Image
import numpy
import numpy as np

class MainWindow():
    def __init__(self, master, title, size):
        self.master = master
        self.title = title
        self.size = size
        self.master.title(self.title)
        self.master.geometry(self.size)
        #Title
        self.main_title=tkinter.Label(self.master, text = "Secure Sending Images",background = 'red',
          foreground ="white",font = ("Times New Roman", 15)).place(x=120,y=0)
        #window
        self.master.resizable(False, False)
        #username label and text entry box
        self.usernameLabel = Label(self.master, text="User Name").place(x=50,y=40)
        self.usernameEntry = Entry(master)
        self.usernameEntry.place(x=200,y=40)
        #password label and password entry box
        self.passwordLabel = Label(self.master,text="Password").place(x=50,y=60)
        self.passwordEntry = Entry(self.master,show='*')
        self.passwordEntry.place(x=200,y=60) 
        #login button
        self.loginButton = Button(self.master, text="Login", command=self.productButtonClicked).place(x=130,y=100)
    def productButtonClicked(self):
        obj = second_window(self,"Welcome  " + self.usernameEntry.get() , "400x600",self.usernameEntry.get(),self.passwordEntry.get())
    def on_cancel(self):
        self.master.destroy() 
        
#=========================================================================================================

class second_window(Toplevel):
    def __init__(self, parent, title, size,username,password):
        if (username == "Alice" and password == "123") or (username == "Bob" and password == "321"):
            super().__init__(name='product_main_menu')
            self.parent = parent
            self.resizable(False, False)
            self.title(title)
            self.size = size
            self.geometry(size)
            self.user_name=username
            self.user_password=password
            self.str=""
            self.str_download_photo=""
            
           #Send title
            self.second_window_title_send=tkinter.Label(self, text = "Sending Images",background = 'red',
                                          foreground ="white",font = ("Times New Roman", 20)).place(x=120,y=0)
            self.info_txt = Label(self, text="1) Enter the user name of the image receiver.").place(x=100,y=40)
            self.info_txt = Label(self, text="2) Choose to load a picture.").place(x=100,y=60)
            self.info_txt = Label(self, text="3) Press Send.").place(x=100,y=80)
            #Send Username 
            self.send_usernameLabel = Label(self, text="1) User Name").place(x=50,y=120)
            self.send_usernameEntry = Entry(self)
            self.send_usernameEntry.place(x=180,y=120)
            #Load text lable
            self.load_text = Label(self, text="2)Choose to load a picture").place(x=50,y=150)
            
            #find_if_user_have_download_photo
            self.str_download_photo = second_window.find_if_user_have_download_photo_(self.user_name)

            if self.str_download_photo == "":
                self.load_text1 = Label(self, text="There is no picture for download").place(x=130,y=350)
            else:
                self.load_text1 = Label(self, text=self.str_download_photo).place(x=130,y=350)
            
            #Open A File
            self.labelFrame = tkinter.LabelFrame(self,text="Open A File")
            self.labelFrame.place(x=70,y=180)
            self.btton()
            
            #Send Button
            self.Send_Button = Button(self,text="Send",width=15,
                                                 command=self.send_image).place(x=130, y=250)
            #Send title
            self.second_window_title_download=tkinter.Label(self, text = "Download Images",background = 'red',
                                          foreground ="white",font = ("Times New Roman", 20)).place(x=110,y=300)
            
            self.downlaod_Button = Button(self,text="Downlaod",width=15,
                                                 command=self.downlaod_image).place(x=130, y=450)
            
            #back button
            self.gobackButton = Button(self,text="Go back to Main Window",width=20,
                                                 command=self.on_cancel).place(x=240, y=570)
        elif username == "" and password == "":
            messagebox.showerror("Error", "Please enter your username and password")
        else:
            messagebox.showerror("Error", "Wrong password or username")
            
#===========================================================================================================================
    
    def send_image(self):
        global index
        if (self.send_usernameEntry.get()) != "" and self.str != "":
            index += 1
            encryptedPlaintext,ckey=user_sender.sendImage(self.str,user_reciver)
            second_window.Add_to_list(self.user_name,self.user_password,self.send_usernameEntry.get(),self.str,encryptedPlaintext,ckey,index)
        else:
            messagebox.showerror("Error!!!", "Enter user name and choose pic, then press Send")
            
        
    def downlaod_image(self):       
        global index
        if self.str_download_photo != "There is no pic for download" and self.str_download_photo != "" :
            encryptedPlaintext=list_of_lists[4][index]
            ckey=list_of_lists[5][index]
            user_reciver.getImageFromSender(user_sender,encryptedPlaintext,ckey)
        else:
             messagebox.showerror("Error!!!", "There is no pic for download")

            
    def on_cancel(self):
        self.destroy()
        
    def btton(self):
        self.button = tkinter.Button(self.labelFrame, text="Browse Afile", command=self.fileDailog)
        self.button.grid(column=1,row=1)
                
    def fileDailog(self):
        self.fileName = filedialog.askopenfilename(initialdir = "/",title = "Select file",
                                    filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        self.label = tkinter.Label(self.labelFrame, text="")
        self.label.grid(column =1,row = 2)
        self.label.configure(text = self.fileName)
        txt = self.fileName 
        Txt = txt.replace("/", " ")
        newtxt = Txt.split()
        if self.fileName != "" :
            self.str=newtxt[len(newtxt)-1]
        else:
            messagebox.showerror("Warning!!", "No Image Selection")
        
        
    def Add_to_list(account_owner_name,account_owner_password,image_receiver_name,user_image,encryptedPlaintext,ckey,index):
        list_of_lists[0].append("")
        list_of_lists[1].append("")
        list_of_lists[2].append("")
        list_of_lists[3].append("")
        list_of_lists[4].append("")
        list_of_lists[5].append("")
        list_of_lists[0][index]= account_owner_name
        list_of_lists[1][index]= image_receiver_name
        list_of_lists[2][index]= account_owner_password
        list_of_lists[3][index]= user_image
        list_of_lists[4][index]= encryptedPlaintext
        list_of_lists[5][index]= ckey
        
    def find_if_user_have_download_photo_(account_owner_name):
        stri=""
        for x in range(len(list_of_lists[1])):
            if  account_owner_name == list_of_lists[1][x]:
                stri =("You have picture from " + list_of_lists[0][x])
        return stri


mainWindow = Tk()
mainFenster = MainWindow(mainWindow, "LOG IN WINDOW", "400x180")
global index
user_sender=User("Alice","123")
user_reciver=User("Bob","321")
index = -1
list_of_lists=[[],[],[],[],[],[]]
mainWindow.mainloop()


