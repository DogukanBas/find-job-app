import tkinter as tk
from tkinter import ttk
from GUI import employeeProfilePage 
from GUI import employeeAdvertisementsPage


def showPage(employeeId):
    root = tk.Tk() 
    #root.resizable(False, False)
    root.title("Main Page") 
    tabControl = ttk.Notebook(root) 
    
    tab1 = ttk.Frame(tabControl) 
    tab2 = ttk.Frame(tabControl)
    
    tabControl.add(tab1, text ='Applications') 
    tabControl.add(tab2, text ='Profile') 
    tabControl.pack(expand = 1, fill ="both") 
     
    employeeAdvertisementsPage.showPage(tab1,employeeId)
    employeeProfilePage.showPage(tab2,employeeId)
    
    
    
    root.mainloop() 