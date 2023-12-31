import tkinter as tk
import employeeSignup
import employerSignup
import employeeMainPage

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
    print(usernameEntry.get())
    print(passwordEntry.get())
    loginForm.destroy()
    employeeMainPage.showPage()

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

loginForm.mainloop()