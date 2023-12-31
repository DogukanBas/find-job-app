import tkinter as tk

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
    employerPasswordEntry = tk.Entry(employerSignupForm)
    employerPasswordEntry.grid(row=4,column=1,padx=5,pady=5)
    
    def submit():
        print(employerNameEntry.get())
        print(employerPhoneEntry.get())
        print(employerAddressEntry.get())
        print(employerUsernameEntry.get())
        print(employerPasswordEntry.get())
        employerSignupForm.destroy()
        
    employerSubmitButton = tk.Button(employerSignupForm,text='Submit',command=submit)
    employerSubmitButton.grid(row=5,column=1,padx=5,pady=5)

    employerSignupForm.mainloop()