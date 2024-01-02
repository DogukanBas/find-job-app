import tkinter as tk
from tkinter import ttk
from Backend import sql_servis as Service
from Backend import Entities

def showPage(tab1,employeeId,root):
    root.geometry("1500x700")
    root.update()
    
    ttk.Label(tab1, text ="By Date").grid(column = 0,  row = 0, padx = 5, pady = 5)
    ttk.Label(tab1, text ="Application Name").grid(column = 1,  row = 0, padx = 5, pady = 5)
    ttk.Label(tab1, text ="Company Name").grid(column = 2,  row = 0, padx = 5, pady = 5)
    ttk.Label(tab1, text ="Position Name").grid(column = 3,  row = 0, padx = 5, pady = 5)
    ttk.Label(tab1, text ="Contract Type").grid(column = 4,  row = 0, padx = 5, pady = 5)   
 
    dateComboBox = ttk.Combobox(tab1,values=('No Filter','Ascending','Descending'))
    dateComboBox.set("No Filter")
    dateComboBox.grid(row=1,column=0,padx=5,pady=5)
    
    applicationNameEntry = tk.Entry(tab1)
    applicationNameEntry.grid(row=1,column=1,padx=5,pady=5)
    
    companyNameEntry = tk.Entry(tab1)
    companyNameEntry.grid(row=1,column=2,padx=5,pady=5)
    
    positionNameEntry = tk.Entry(tab1)
    positionNameEntry.grid(row=1,column=3,padx=5,pady=5)
    
    contractTypeComboBox = ttk.Combobox(tab1,values=('No Filter','Full Time','Part Time','Intern'))
    contractTypeComboBox.set('No Filter')
    contractTypeComboBox.grid(row=1,column=4,padx=5,pady=5)
    
    def filter():
        filter = Entities.Filter(dateComboBox.get(),applicationNameEntry.get(),companyNameEntry.get(),positionNameEntry.get(),contractTypeComboBox.get())
        pass
    
    filterButton = tk.Button(tab1,text='Filter',command=filter)
    filterButton.grid(row=2,column=2,padx=5,pady=5)
    
    applicationColumns = ('Application Id','Application Name', 'Application Date','Counter','Contract Type', 'Position Name','Description')
    applicationListView = ttk.Treeview(tab1, columns=applicationColumns, show='headings')

    # set column headings
    for col in applicationColumns:
        applicationListView.heading(col, text=col)

    applicationList = Service.showAllApplications()
    
    for app in applicationList: 
        applicationListView.insert('', 'end', text="1", values=(app.applicationId , app.applicationName, app.applicationDate, app.counter, app.contractType,app.positionName,app.description))
        
    applicationListView.grid(row=3,padx=5,pady=5,columnspan=5)
    
    scrollbarApplications = tk.Scrollbar(tab1, orient=tk.VERTICAL, command=applicationListView.yview)
    applicationListView.configure(yscrollcommand=scrollbarApplications.set)
    scrollbarApplications.grid(row=5,column=3, sticky='ns',padx=5,pady=5)
    
    def apply():
        pass
        # selectedApplication = applicationListView.item(applicationListView.selection())['values']
        # if(selectedApplication == ""):
        #     print("No application selected")
        #     return
        # else:
        #     print(selectedApplication)
        #     newApplication = Entities.Application(employeeId,selectedApplication[0],selectedApplication[3]+1,selectedApplication[1],None,selectedApplication[4],selectedApplication[5],selectedApplication[6])
        #     status = Service.applyToApplication(newApplication)
        #     if(status == True):
        #         print("Application successful")
        #         #messagebox.showinfo("Apply", "Application successful")
        #     else:
        #         print("Application failed")
        #         #messagebox.showerror("Apply", f"Application failed - {status}")
    
    applyButton = tk.Button(tab1,text='Apply',command=apply)
    applyButton.grid(row=6,column=2,padx=5,pady=5)
    
    
    
    
    
    