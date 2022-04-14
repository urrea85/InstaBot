from tkinter import *
from tkinter.ttk import Combobox
from tkinter import scrolledtext
import tkinter as tk
from tkinter import messagebox
from tkinter import Menu
from insta import *

def logIn(): 
	if username.get() == "" or password.get() == "":
		messagebox.showinfo('ERROR','Complete the data')
	else:
		browser = webdriver.Chrome()
		browser.get("https://www.instagram.com/")
		sleep(2)
		accept_cookies(browser)
		login(browser,username.get(),password.get())
		browser.quit()

root = Tk()
root.title("InstaBot")

#username label and text entry box
usernameLabel = Label(root, text="User Name", font=("Arial Bold", 20), fg="purple").grid(row=0, column=0)
username = StringVar()
usernameEntry = Entry(root, textvariable=username).grid(row=0, column=1)  

#password label and password entry box
passwordLabel = Label(root,text="Password", font=("Arial Bold", 20), fg="purple").grid(row=1, column=0)  
password = StringVar()
passwordEntry = Entry(root, textvariable=password, show='*').grid(row=1, column=1)  

loginButton = Button(root, text="Login", command=logIn).grid(row=4, column=0) 



root.mainloop()

"""browser = webdriver.Chrome()
browser.get("https://www.instagram.com/")
sleep(2)

accept_cookies(browser)
browser.quit() """



#TAMBIEN TENEMOS Checkbutton y Radiobutton
#https://likegeeks.com/es/ejemplos-de-la-gui-de-python/#Crear_tu_primera_aplicacion_GUI