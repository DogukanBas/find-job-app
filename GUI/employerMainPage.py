import tkinter as tk
from tkinter import ttk
from Backend import sql_servis as Service
from Backend import Entities
from tkinter import messagebox
from tkinter.ttk import Combobox

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
        applicationListView.column(col,minwidth=10,width=150)
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
            newApplication = Entities.Application(employerId,None,None,applicationNameEntry.get(),None,comboText.get(),positionNameEntry.get(),descriptionEntry.get("1.0","end-1c"),True)
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
            app = Entities.Application(employerId,applicationValues[0],applicationValues[3],updateField[0].get(),applicationValues[2],updateField[1].get(),updateField[2].get(),descriptionEntry.get("1.0","end-1c"),True)
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
        application = Entities.Application(employerId,applicationValues[0],applicationValues[3],applicationValues[1],applicationValues[2],applicationValues[4],applicationValues[5],applicationValues[6],False)
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
        
        status , applicantsList = Service.getApplicantsView(applicationId)
        if status == True:
            print("Applicants retrieved")
            print(applicantsList)
        else:
            print(status)
            #messagebox.showinfo("Applicants", status) 
            return
        
        applicantsTop = tk.Toplevel()
        applicantsTop.title('Applicants')
        applicantsTop.resizable(False,False)
            
        applicantsColumns = ('Application Id','Employee Id','Employee Name', 'Employee Surname','Employee Phone','Employee Address', 'Apply Date','Status')
        applicantsListView = ttk.Treeview(applicantsTop, columns=applicantsColumns, show='headings')

        # set column headings
        for col in applicantsColumns:
            applicantsListView.column(col,minwidth=10,width=100)
            applicantsListView.heading(col, text=col)

        if status == True:
            print("Applicants retrieved")
            print(applicantsList)
            for app in applicantsList: 
                applicantsListView.insert('', 'end', text="1", values=(app.applicationId , app.employeeId,app.employeeName,app.employeeSurname, app.employeePhone, app.employeeAddress,app.applicationDate,app.status))
        else:   
            print(status)
            #messagebox.showinfo("Applications", status)
            
        applicantsListView.grid(row=0,padx=5,pady=5,columnspan=3)
        
        scrollbarApplicants = ttk.Scrollbar(applicantsTop, orient=tk.VERTICAL, command=applicantsListView.yview)
        applicantsListView.configure(yscrollcommand=scrollbarApplicants.set)
        scrollbarApplicants.grid(row=0,column=3, sticky='ns',padx=5,pady=5) 
        
        def showDetailsTopLevel():
            selectedApplicant = applicantsListView.selection()[0]
            applicantValues = applicantsListView.item(selectedApplicant)['values']
            employeeId = applicantValues[1]
            applicationId = applicantValues[0]
            
            detailsTop = tk.Toplevel()
            detailsTop.title('Details')
            detailsTop.geometry('850x700')
            detailsTop.resizable(False,False)
            
            canvas = tk.Canvas(detailsTop)
            scrollbar = ttk.Scrollbar(detailsTop, orient="vertical", command=canvas.yview, style='Vertical.TScrollbar')
            scrollable_frame = ttk.Frame(canvas)
            scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
            ) 

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
  
            ttk.Label(scrollable_frame,text="Education Information",font="Times 30").grid(row=0,column=0,padx=5,pady=5)
    
            schoolColumns = ('School Name', 'School Type', 'Start Date','End Date')
            schoolList = ttk.Treeview(scrollable_frame, columns=schoolColumns, show='headings')

            # set column headings
            for col in schoolColumns:
                schoolList.heading(col, text=col)

            educationList = Service.getEducation(employeeId)
            
            for edu in educationList: 
                schoolList.insert('', 'end', text="1", values=(edu.schoolName, edu.schoolType, edu.startDate, edu.endDate))
            
            # Insert the data in Treeview widget
            schoolList.grid(row=1,padx=5,pady=5)
            
            scrollbarSchool = ttk.Scrollbar(scrollable_frame, orient=tk.VERTICAL, command=schoolList.yview)
            schoolList.configure(yscrollcommand=scrollbarSchool.set)
            scrollbarSchool.grid(row=1,column=1, sticky='ns',padx=5,pady=5)
            
            ttk.Label(scrollable_frame,text="Experience Information",font="Times 30").grid(row=2,column=0,padx=5,pady=5)
            
            experienceColumns = ('Company Name', 'Position', 'Start Date','End Date')
            experienceList = ttk.Treeview(scrollable_frame, columns=experienceColumns, show='headings')

            for col in experienceColumns:
                experienceList.heading(col, text=col)

            experiences = Service.getExperience(employeeId)
            
            for exp in experiences: 
                experienceList.insert('', 'end', text="1", values=(exp.companyName, exp.positionName, exp.startDate, exp.endDate))
            
            experienceList.grid(row=3,padx=5,pady=5)
            
            scrollbarExperience = ttk.Scrollbar(scrollable_frame, orient=tk.VERTICAL, command=experienceList.yview)
            experienceList.configure(yscrollcommand=scrollbarExperience.set)
            scrollbarExperience.grid(row=3,column=1, sticky='ns',padx=5,pady=5)
            
            ttk.Label(scrollable_frame,text="Cover Letter",font="Times 30").grid(row=4,column=0,padx=5,pady=5)
            
            coverLetterEntry = tk.Text(scrollable_frame,width=70)
            
            for app in applicantsList: 
                if app.employeeId == employeeId:
                    coverLetter = app.coverLetter
                    coverLetterEntry.insert(tk.INSERT, coverLetter)
                    break
            coverLetterEntry.config(state='disabled')
            coverLetterEntry.grid(row=5,column=0,padx=5,pady=5)
            
            def approveApplication():
                status = Service.evaluate(applicationId,employeeId,True)
                if status == True:
                    print("Application approved")
                    #messagebox.showinfo("Application Approve", "Application approved")
                    applicantsListView.delete(*applicantsListView.get_children())
                    status , applicantsList = Service.getApplicantsView(applicationId)
                    if status != True:
                        #messagebox.showinfo("Error while reloading table", "Error while reloading table")
                        return
                    for app in applicantsList: 
                        applicantsListView.insert('', 'end', text="1", values=(app.applicationId , app.employeeId,app.employeeName,app.employeeSurname, app.employeePhone, app.employeeAddress,app.applicationDate,app.status))
                    detailsTop.destroy()
                else:
                    print(status)
                    #messagebox.showinfo("Application Approve", status)
            
            def rejectApplication():
                status = Service.evaluate(applicationId,employeeId,False)
                if status == True:
                    print("Application rejected")
                    #messagebox.showinfo("Application Reject", "Application rejected")
                    applicantsListView.delete(*applicantsListView.get_children())
                    status , applicantsList = Service.getApplicantsView(applicationId)
                    if status != True:
                        #messagebox.showinfo("Error while reloading table", "Error while reloading table")
                        return
                    for app in applicantsList: 
                        applicantsListView.insert('', 'end', text="1", values=(app.applicationId , app.employeeId,app.employeeName,app.employeeSurname, app.employeePhone, app.employeeAddress,app.applicationDate,app.status))
                    detailsTop.destroy()
                else:
                    print(status)
                    #messagebox.showinfo("Application Reject", status)
            
            approveButton = tk.Button(scrollable_frame,text='Approve',command=approveApplication)
            approveButton.grid(row=6,column=0,padx=5,pady=5)
            
            rejectButton = tk.Button(scrollable_frame,text='Reject',command=rejectApplication)
            rejectButton.grid(row=7,column=0,padx=5,pady=5)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
    
        
        showDetailButton = tk.Button(applicantsTop,text='Show Details and Evaluate',command=showDetailsTopLevel)
        showDetailButton.grid(row=1,column=1,padx=5,pady=5) 
        
        
            
    
    
    addApplicationButton = tk.Button(root,text='Add',command=addApplicationTopLevel)
    addApplicationButton.grid(row=7,column=0,padx=5,pady=5)
    updateApplicationButton = tk.Button(root,text='Update',command=updateApplicationTopLevel)
    updateApplicationButton.grid(row=7,column=1,padx=5,pady=5)
    deleteApplicationButton = tk.Button(root,text='Delete',command=deleteApplicationTopLevel)
    deleteApplicationButton.grid(row=7,column=2,padx=5,pady=5)
    showApplicantsButton = tk.Button(root,text='Show Applicants',command=showApplicantsTopLevel)
    showApplicantsButton.grid(row=8,column=1,padx=5,pady=5)

    
    root.mainloop()