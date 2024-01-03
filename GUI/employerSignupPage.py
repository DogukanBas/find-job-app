import tkinter as tk
from tkinter import messagebox
import Backend.Entities as Entities
import Backend.sql_servis as Service

def showPage() :
    employerSignupForm = tk.Tk()
    employerSignupForm.title('Employer Signup')
    employerSignupForm.resizable(False,False)

    employerSignupForm.columnconfigure(0, weight=1)
    employerSignupForm.columnconfigure(1, weight=3)

    employerNameLabel = tk.Label(employerSignupForm,text='Name: ')
    employerNameLabel.grid(row=0,column=0,padx=5,pady=5)
    employerPhoneLabel = tk.Label(employerSignupForm,text='Phone: ')
    employerPhoneLabel.grid(row=1,column=0,padx=5,pady=5)
    employerAddressLabel = tk.Label(employerSignupForm,text='Address: ')
    employerAddressLabel.grid(row=2,column=0,padx=5,pady=5)
    employerUsernameLabel = tk.Label(employerSignupForm,text='Username: ')
    employerUsernameLabel.grid(row=3,column=0,padx=5,pady=5)
    employerPasswordLabel = tk.Label(employerSignupForm,text='Password: ')
    employerPasswordLabel.grid(row=4,column=0,padx=5,pady=5)
    
    #add entrys to the right of all labels
    employerNameEntry = tk.Entry(employerSignupForm)
    employerNameEntry.grid(row=0,column=1,padx=5,pady=5)
    employerPhoneEntry = tk.Entry(employerSignupForm)
    employerPhoneEntry.grid(row=1,column=1,padx=5,pady=5)
    employerAddressEntry = tk.Entry(employerSignupForm)
    employerAddressEntry.grid(row=2,column=1,padx=5,pady=5)
    employerUsernameEntry = tk.Entry(employerSignupForm)
    employerUsernameEntry.grid(row=3,column=1,padx=5,pady=5)
    employerPasswordEntry = tk.Entry(employerSignupForm,show='*')
    employerPasswordEntry.grid(row=4,column=1,padx=5,pady=5)
    
    def submit():
        newAccount = Entities.Account(None,employerUsernameEntry.get(),employerPasswordEntry.get(),False)
        newEmployer = Entities.Employer(None,employerNameEntry.get(),employerPhoneEntry.get(),employerAddressEntry.get())
        status = Service.registerEmployer(newEmployer,newAccount)
        if(status == True):
            print("Employer registered")
            messagebox.showinfo("Employer Signup", "Employer registered")
            employerSignupForm.destroy()
        else:
            print("Employer registration failed")
            messagebox.showerror("Employer Signup", f"Employer registration failed - {status}")
        
    employerSubmitButton = tk.Button(employerSignupForm,text='Submit',command=submit)
    employerSubmitButton.grid(row=5,column=1,padx=5,pady=5)

    employerSignupForm.mainloop()