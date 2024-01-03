import tkinter as tk
from tkinter import ttk
from Backend import sql_servis as Service
from Backend import Entities
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkcalendar import Calendar
from datetime import datetime

def showPage(employerId):
    root = tk.Tk() 
    root.title("Employer Main Page") 
    
    status, employer = Service.getEmployerInfo(employerId)
    if status == True:
        print("Employer info retrieved")
        print(type(employer))
        print(employer.employerName)
    else:
        print(status)
        #messagebox.showinfo("Employer Info", status)
        return
    
    tk.Label(root, text ="Name:").grid(column = 0,  row = 0, padx = 5, pady = 5) 
    tk.Label(root, text ="Phone:").grid(column = 0,  row = 1, padx = 5, pady = 5)
    tk.Label(root, text ="Address:").grid(column = 0,  row = 2, padx = 5, pady = 5) 
    
    employerName = tk.StringVar()
    employerName.set(employer.employerName)
    employerAddress = tk.StringVar()
    employerAddress.set(employer.employerAdress)
    employerPhone = tk.StringVar()
    employerPhone.set(employer.employerPhone)
    
    nameEntry = tk.Entry(root,textvariable=employerName)
    nameEntry.grid(row=0,column=1,padx=5,pady=5)
    phoneEntry = tk.Entry(root,textvariable=employerPhone)
    phoneEntry.grid(row=1,column=1,padx=5,pady=5)
    addressEntry = tk.Entry(root,textvariable=employerAddress)
    addressEntry.grid(row=2,column=1,padx=5,pady=5)

    def updateInfos():
        newEmployer = Entities.Employer(employerId,employerName.get(),employerPhone.get(),employerAddress.get())
        status = Service.updateEmployerInfo(newEmployer)
        if status == True:
            print("Employer info updated")
            #messagebox.showinfo("Employer Info", "Employer info updated")
        else:
            print(status)
            #messagebox.showinfo("Employer Info", status)
    
    saveButton = tk.Button(root,text='Save',command=updateInfos)
    saveButton.grid(row=3,column=1,padx=5,pady=5)
    
    tk.Label(root,text="Applications",font="Times 30").grid(row=4,column=1,padx=5,pady=5)
    
    applicationColumns = ('Application Id','Application Name', 'Application Date','Counter','Contract Type', 'Position Name','Description')
    applicationListView = ttk.Treeview(root, columns=applicationColumns, show='headings')

    # set column headings
    for col in applicationColumns:
        applicationListView.heading(col, text=col)

    applicationList = Service.getApplications(employerId)
    
    for app in applicationList: 
        applicationListView.insert('', 'end', text="1", values=(app.applicationId , app.applicationName, app.applicationDate, app.counter, app.contractType,app.positionName,app.description))
        
    applicationListView.grid(row=5,padx=5,pady=5,columnspan=3)
    
    scrollbarApplications = ttk.Scrollbar(root, orient=tk.VERTICAL, command=applicationListView.yview)
    applicationListView.configure(yscrollcommand=scrollbarApplications.set)
    scrollbarApplications.grid(row=5,column=3, sticky='ns',padx=5,pady=5)
    
    def addApplicationTopLevel():
        addApplicationTop = tk.Toplevel()
        addApplicationTop.title('Add Application')
        addApplicationTop.resizable(False,False)
        
        addApplicationTop.columnconfigure(0, weight=1)
        addApplicationTop.columnconfigure(1, weight=3)
        
        applicationNameLabel = tk.Label(addApplicationTop,text='Application Name: ')
        applicationNameLabel.grid(row=0,column=0,padx=5,pady=5)
        contractTypeLabel = tk.Label(addApplicationTop,text='Contract Type: ')
        contractTypeLabel.grid(row=1,column=0,padx=5,pady=5)
        positionNameLabel = tk.Label(addApplicationTop,text='Position Name: ')
        positionNameLabel.grid(row=2,column=0,padx=5,pady=5)
        descriptionLabel = tk.Label(addApplicationTop,text='Description: ')
        descriptionLabel.grid(row=3,column=0,padx=5,pady=5)
        
        applicationNameEntry = tk.Entry(addApplicationTop)
        applicationNameEntry.grid(row=0,column=1,padx=5,pady=5)
        comboText = tk.StringVar()
        comboText.set('Part Time')
        contractTypeComboBox = Combobox(addApplicationTop,values=('Part Time','Full Time','Intern'),textvariable=comboText,state='readonly')
        contractTypeComboBox.grid(row=1,column=1,padx=5,pady=5)
        positionNameEntry = tk.Entry(addApplicationTop)
        positionNameEntry.grid(row=2,column=1,padx=5,pady=5)
        descriptionEntry = tk.Text(addApplicationTop)
        descriptionEntry.grid(row=3,column=1,padx=5,pady=5)
        
        def submitApplication():
            newApplication = Entities.Application(employerId,None,None,applicationNameEntry.get(),None,comboText.get(),positionNameEntry.get(),descriptionEntry.get("1.0","end-1c"))
            status, app = Service.addApplication(newApplication)
            if status == True:
                print("Application added")
                #messagebox.showinfo("Add Application", "Application added")
                applicationListView.insert('','end',values=(app.applicationId,app.applicationName,app.applicationDate,app.counter,app.contractType,app.positionName,app.description))
                addApplicationTop.destroy()
            else:
                print(status)
                #messagebox.showinfo("Add Application", status)
                
        submitButton = tk.Button(addApplicationTop,text='Submit',command=submitApplication)
        submitButton.grid(row=4,column=1,padx=5,pady=5)
        
    def updateApplicationTopLevel():
        selectedApplication = applicationListView.selection()[0]
        applicationValues = applicationListView.item(selectedApplication)['values']
        print(applicationValues)
        updateApplicationTop = tk.Toplevel()
        updateApplicationTop.title('Update Application')
        updateApplicationTop.resizable(False,False)
        updateField = []
        updateField.append(tk.StringVar())
        updateField.append(tk.StringVar())
        updateField.append(tk.StringVar())
        updateField.append(tk.StringVar())
        updateField[0].set(applicationValues[1])
        updateField[1].set(applicationValues[4])
        updateField[2].set(applicationValues[5])
        updateField[3].set(applicationValues[6])
        
        updateApplicationTop.columnconfigure(0, weight=1)
        updateApplicationTop.columnconfigure(1, weight=3)
        
        def updateApplication():
            app = Entities.Application(employerId,applicationValues[0],applicationValues[3],updateField[0].get(),applicationValues[2],updateField[1].get(),updateField[2].get(),descriptionEntry.get("1.0","end-1c"))
            status = Service.updateApplication(app)
            if status == True:
                print("Application updated")
                #messagebox.showinfo("Application Update", "Application updated")
                applicationListView.item(selectedApplication,values=(app.applicationId,app.applicationName,app.applicationDate,app.counter,app.contractType,app.positionName,app.description))
                updateApplicationTop.destroy()
            else:
                print(status)
                #messagebox.showinfo("Application Update", status)
        
        applicationNameLabel = tk.Label(updateApplicationTop,text='Application Name: ')
        applicationNameLabel.grid(row=0,column=0,padx=5,pady=5)
        contractTypeLabel = tk.Label(updateApplicationTop,text='Contract Type: ')
        contractTypeLabel.grid(row=1,column=0,padx=5,pady=5)
        positionNameLabel = tk.Label(updateApplicationTop,text='Position Name: ')
        positionNameLabel.grid(row=2,column=0,padx=5,pady=5)
        descriptionLabel = tk.Label(updateApplicationTop,text='Description: ')
        descriptionLabel.grid(row=3,column=0,padx=5,pady=5)
        updateApplicationButton = tk.Button(updateApplicationTop,text='Update',command=updateApplication)
        updateApplicationButton.grid(row=4,column=1,padx=5,pady=5)
        
        applicationNameEntry = tk.Entry(updateApplicationTop,textvariable=updateField[0])
        applicationNameEntry.grid(row=0,column=1,padx=5,pady=5)
        comboText = tk.StringVar()
        comboText = updateField[1]
        contractTypeComboBox = Combobox(updateApplicationTop,values=('Part Time','Full Time','Intern'),textvariable=comboText,state='readonly')
        contractTypeComboBox.grid(row=1,column=1,padx=5,pady=5)
        positionNameEntry = tk.Entry(updateApplicationTop,textvariable=updateField[2])
        positionNameEntry.grid(row=2,column=1,padx=5,pady=5)
        descriptionEntry = tk.Text(updateApplicationTop)
        descriptionEntry.insert(tk.INSERT, updateField[3].get())
        descriptionEntry.grid(row=3,column=1,padx=5,pady=5)
        
        
        
        
    
    def deleteApplicationTopLevel():
        selectedApplication = applicationListView.selection()[0]
        applicationValues = applicationListView.item(selectedApplication)['values']
        application = Entities.Application(employerId,applicationValues[0],applicationValues[3],applicationValues[1],applicationValues[2],applicationValues[4],applicationValues[5],applicationValues[6])
        status = Service.deleteApplication(application)
        if status == True:
            print("Application deleted")
            #messagebox.showinfo("Application Delete", "Application deleted")
            applicationListView.delete(selectedApplication)
        else:
            print(status)
            #messagebox.showinfo("Application Delete", status)
    
    def showApplicantsTopLevel():
        selectedApplication = applicationListView.selection()[0]
        applicationValues = applicationListView.item(selectedApplication)['values']
        applicationId = applicationValues[0]
        pass
    
        
    
    addApplicationButton = tk.Button(root,text='Add',command=addApplicationTopLevel)
    addApplicationButton.grid(row=7,column=0,padx=5,pady=5)
    updateApplicationButton = tk.Button(root,text='Update',command=updateApplicationTopLevel)
    updateApplicationButton.grid(row=7,column=1,padx=5,pady=5)
    deleteApplicationButton = tk.Button(root,text='Delete',command=deleteApplicationTopLevel)
    deleteApplicationButton.grid(row=7,column=2,padx=5,pady=5)
    showApplicantsButton = tk.Button(root,text='Show Applicants')
    showApplicantsButton.grid(row=8,column=1,padx=5,pady=5)

    
    root.mainloop()