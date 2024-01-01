import tkinter as tk
from tkinter import ttk
from GUI import employeeProfile 
from GUI import employeeAdvertisements


def showPage():
    root = tk.Tk() 
    root.title("Main Page") 
    tabControl = ttk.Notebook(root) 
    
    tab1 = ttk.Frame(tabControl) 
    tab2 = ttk.Frame(tabControl) 
    
    tabControl.add(tab1, text ='Advertisements') 
    tabControl.add(tab2, text ='Profile') 
    tabControl.pack(expand = 1, fill ="both") 
     
    employeeAdvertisements.showPage(tab1)
    employeeProfile.showPage(tab2)
    
    
    
    root.mainloop() 