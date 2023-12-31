import tkinter as tk

def showPage() :
    employeeSignupForm = tk.Tk()
    employeeSignupForm.title('Employee Signup')
    employeeSignupForm.resizable(False,False)

    employeeSignupForm.columnconfigure(0, weight=1)
    employeeSignupForm.columnconfigure(1, weight=3)

    employeeNameLabel = tk.Label(employeeSignupForm,text='Name: ')
    employeeNameLabel.grid(row=0,column=0,padx=5,pady=5)
    employeeSurnameLabel = tk.Label(employeeSignupForm,text='Surname: ')
    employeeSurnameLabel.grid(row=1,column=0,padx=5,pady=5)
    employeePhoneLabel = tk.Label(employeeSignupForm,text='Phone: ')
    employeePhoneLabel.grid(row=2,column=0,padx=5,pady=5)
    employeeAddressLabel = tk.Label(employeeSignupForm,text='Address: ')
    employeeAddressLabel.grid(row=3,column=0,padx=5,pady=5)
    employeeUsernameLabel = tk.Label(employeeSignupForm,text='Username: ')
    employeeUsernameLabel.grid(row=4,column=0,padx=5,pady=5)
    employeePasswordLabel = tk.Label(employeeSignupForm,text='Password: ')
    employeePasswordLabel.grid(row=5,column=0,padx=5,pady=5)
    
    employeeNameEntry = tk.Entry(employeeSignupForm)
    employeeNameEntry.grid(row=0,column=1,padx=5,pady=5)
    employeeSurnameEntry = tk.Entry(employeeSignupForm)
    employeeSurnameEntry.grid(row=1,column=1,padx=5,pady=5)
    employeePhoneEntry = tk.Entry(employeeSignupForm)
    employeePhoneEntry.grid(row=2,column=1,padx=5,pady=5)
    employeeAddressEntry = tk.Entry(employeeSignupForm)
    employeeAddressEntry.grid(row=3,column=1,padx=5,pady=5)
    employeeUsernameEntry = tk.Entry(employeeSignupForm)
    employeeUsernameEntry.grid(row=4,column=1,padx=5,pady=5)
    employeePasswordEntry = tk.Entry(employeeSignupForm)
    employeePasswordEntry.grid(row=5,column=1,padx=5,pady=5)
    
    def submit():
        print(employeeNameEntry.get())
        print(employeeSurnameEntry.get())
        print(employeePhoneEntry.get())
        print(employeeAddressEntry.get())
        print(employeeUsernameEntry.get())
        print(employeePasswordEntry.get())
        employeeSignupForm.destroy()
    
    submitButton = tk.Button(employeeSignupForm, text="Submit", command=submit)
    submitButton.grid(row=6,column=1,padx=5,pady=5)
        

    employeeSignupForm.mainloop()
        
    
    