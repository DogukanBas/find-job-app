import tkinter as tk
from tkinter import messagebox
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
print(sys.path)
from GUI import employeeMainPage
from GUI import employerSignup
from GUI import employeeSignup
import Backend.sql_servis as Service
import Backend.sql_servis as Entities


loginForm = tk.Tk()
loginForm.title('Login Page')
loginForm.resizable(False,False)

loginForm.columnconfigure(0, weight=1)
loginForm.columnconfigure(1, weight=3)

usernameLabel = tk.Label(loginForm,text='Username:')
usernameLabel.grid(column=0,row=0,padx=5,pady=5)
passwordLabel = tk.Label(loginForm,text='Password:')
passwordLabel.grid(column=0,row=1,padx=5,pady=5)

usernameEntry = tk.Entry(loginForm)
usernameEntry.grid(column=1,row=0,padx=5,pady=5)

passwordEntry = tk.Entry(loginForm,show='*')
passwordEntry.grid(column=1,row=1,padx=5,pady=5)

def login():
    account = Entities.Account(None,usernameEntry.get(),passwordEntry.get(),None)
    status = Service.loginCheck(account)
    
    if(status == "No such user"):
        print("No such user")
        messagebox.showinfo("Login Failed", status)
        return
    elif(status == "Employee"):
        print("Employee")
        employeeMainPage.showPage()
        loginForm.destroy()
    elif(status == "Employer"):
        print("Employer")
        #employerMainPage.showPage()
        #loginForm.destroy()
    elif(status == "Username and password cannot be empty."):
        print("Error")
        messagebox.showinfo(title="Login Failed", message = status)
    else:
        print("xd")
        messagebox.showinfo("Login Failed", status)
        return

def showPage():
    loginForm.mainloop()

loginButton = tk.Button(loginForm,text='Login',command=login)
loginButton.grid(column=1,row=2)



employeeSignUpLabel = tk.Label(loginForm,text='Employee signup',fg='white',font=('Times 15 underline'))
employeeSignUpLabel.grid(column=0,row=3,padx=5,pady=5)
employeeSignUpLabel.bind("<Button-1>", lambda e: employeeSignup.showPage())
employeeSignUpLabel.bind("<Enter>", lambda e: e.widget.configure(fg='blue'))
employeeSignUpLabel.bind("<Leave>", lambda e: e.widget.configure(fg='white'))

employerSignUpLabel = tk.Label(loginForm,text='Employer signup',fg='white',font=('Times 15 underline'))
employerSignUpLabel.grid(column=1,row=3,padx=5,pady=5)
employerSignUpLabel.bind("<Button-1>", lambda e: employerSignup.showPage())
employerSignUpLabel.bind("<Enter>", lambda e: e.widget.configure(fg='blue'))
employerSignUpLabel.bind("<Leave>", lambda e: e.widget.configure(fg='white'))
