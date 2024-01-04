import tkinter as tk
from tkinter import ttk
from Backend import sql_servis as Service
from Backend import Entities
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkcalendar import Calendar
from datetime import datetime
from tkinter import Scrollbar


def showPage(tab2,employeeId):
    canvas = tk.Canvas(tab2)
    scrollbar = ttk.Scrollbar(tab2, orient="vertical", command=canvas.yview, style='Vertical.TScrollbar')
    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
) 

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    

    status, employee = Service.getEmployeeInfo(employeeId)
    if status == True:
        print("Employee info retrieved")
        print(type(employee))
        print(employee.employeeName)
    else:
        print(status)
        #messagebox.showinfo("Employee Info", status)
        return
    
    ttk.Label(scrollable_frame, text ="Name:").grid(column = 0,  row = 0, padx = 5, pady = 5) 
    ttk.Label(scrollable_frame, text ="Surname:").grid(column = 0,  row = 1, padx = 5, pady = 5) 
    ttk.Label(scrollable_frame, text ="Address:").grid(column = 0,  row = 2, padx = 5, pady = 5) 
    ttk.Label(scrollable_frame, text ="Phone:").grid(column = 0,  row = 3, padx = 5, pady = 5) 
    
    
    
    employeeName = tk.StringVar()
    employeeName.set(employee.employeeName)
    employeeSurname = tk.StringVar()
    employeeSurname.set(employee.employeeSurname)
    employeeAddress = tk.StringVar()
    employeeAddress.set(employee.employeeAddress)
    employeePhone = tk.StringVar()
    employeePhone.set(employee.employeePhone)

    nameEntry = tk.Entry(scrollable_frame,textvariable=employeeName)
    nameEntry.grid(row=0,column=1,padx=5,pady=5)
    surnameEntry = tk.Entry(scrollable_frame,textvariable=employeeSurname)
    surnameEntry.grid(row=1,column=1,padx=5,pady=5)
    addressEntry = tk.Entry(scrollable_frame,textvariable=employeeAddress)
    addressEntry.grid(row=2,column=1,padx=5,pady=5)
    phoneEntry = tk.Entry(scrollable_frame,textvariable=employeePhone)
    phoneEntry.grid(row=3,column=1,padx=5,pady=5)

    def updateInfos():
        newEmployee = Entities.Employee(employeeId,employeeName.get(),employeeSurname.get(),employeePhone.get(),employeeAddress.get())
        status = Service.updateEmployeeInfo(newEmployee)
        if status == True:
            print("Employee info updated")
            #messagebox.showinfo("Employee Info", "Employee info updated")
        else:
            print(status)
            #messagebox.showinfo("Employee Info", status)
    
    saveButton = ttk.Button(scrollable_frame,text='Save',command=updateInfos)
    saveButton.grid(row=4,column=1,padx=5,pady=5)
    
    #list past experiences in multi column list
    
    ttk.Label(scrollable_frame,text="Education Information",font="Times 30").grid(row=5,column=1,padx=5,pady=5)
    
    schoolColumns = ('School Name', 'School Type', 'Start Date','End Date')
    schoolList = ttk.Treeview(scrollable_frame, columns=schoolColumns, show='headings')

    # set column headings
    for col in schoolColumns:
        schoolList.heading(col, text=col)

    educationList = Service.getEducation(employeeId)
    
    for edu in educationList: 
        schoolList.insert('', 'end', text="1", values=(edu.schoolName, edu.schoolType, edu.startDate, edu.endDate))
        
   

     
    # Insert the data in Treeview widget
    schoolList.grid(row=6,padx=5,pady=5,columnspan=3)
    
    scrollbarSchool = ttk.Scrollbar(scrollable_frame, orient=tk.VERTICAL, command=schoolList.yview)
    schoolList.configure(yscrollcommand=scrollbarSchool.set)
    scrollbarSchool.grid(row=6,column=3, sticky='ns',padx=5,pady=5)
    
    #add, update, delete buttons for school list
    def addSchoolTopLevel():
        addSchoolTop = tk.Toplevel()
        addSchoolTop.title('Add School')
        addSchoolTop.resizable(False,False)
        
        addSchoolTop.columnconfigure(0, weight=1)
        addSchoolTop.columnconfigure(1, weight=3)
        
        schoolNameLabel = tk.Label(addSchoolTop,text='School Name: ')
        schoolNameLabel.grid(row=0,column=0,padx=5,pady=5)
        schoolTypeLabel = tk.Label(addSchoolTop,text='School Type: ')
        schoolTypeLabel.grid(row=1,column=0,padx=5,pady=5)
        startDateLabel = tk.Label(addSchoolTop,text='Start Date: ')
        startDateLabel.grid(row=2,column=0,padx=5,pady=5)
        endDateLabel = tk.Label(addSchoolTop,text='End Date: ')
        endDateLabel.grid(row=3,column=0,padx=5,pady=5)
        
        schoolNameEntry = tk.Entry(addSchoolTop)
        schoolNameEntry.grid(row=0,column=1,padx=5,pady=5)
        comboText = tk.StringVar()
        comboText.set("Bachelors")
        schoolTypeComboBox = Combobox(addSchoolTop,values=('High School','Bachelors','Masters'),textvariable=comboText,state='readonly')
        schoolTypeComboBox.grid(row=1,column=1,padx=5,pady=5)
        startDateCalendar = Calendar(addSchoolTop)
        startDateCalendar.grid(row=2,column=1,padx=5,pady=5)
        endDateCalendar = Calendar(addSchoolTop)
        endDateCalendar.grid(row=3,column=1,padx=5,pady=5)
        
        def submitSchool():
            print(startDateCalendar.selection_get())
            print(endDateCalendar.selection_get())

            newEducation = Entities.Education(employeeId,schoolNameEntry.get(),startDateCalendar.selection_get(),endDateCalendar.selection_get(),comboText.get())
            status = Service.addEducation(newEducation)
            if(status == True):
                print("School added")
                #messagebox.showinfo("School Add", "School added")
                schoolList.insert('','end',values=(schoolNameEntry.get(),comboText.get(),startDateCalendar.selection_get(),endDateCalendar.selection_get()))
                addSchoolTop.destroy()
            else: 
                print(status)
                #messagebox.showinfo("School Add", status)
                
            
        submitButton = tk.Button(addSchoolTop,text='Submit',command=submitSchool)
        submitButton.grid(row=4,column=1,padx=5,pady=5)
        
    def deleteSchool():
        selectedSchool = schoolList.selection()[0]
        schoolValues = schoolList.item(selectedSchool)['values']
        education = Entities.Education(employeeId,schoolValues[0],schoolValues[2],schoolValues[3],schoolValues[1])
        status = Service.deleteEducation(education)
        if status == True:
            print("School deleted")
            #messagebox.showinfo("School Delete", "School deleted")
            schoolList.delete(selectedSchool)
        else:
            print(status)
            #messagebox.showinfo("School Delete", status)
    
    def updateSchoolTopLevel():
        selectedSchool = schoolList.selection()[0]
        schoolValues = schoolList.item(selectedSchool)['values']
        print(schoolValues)
        updateSchoolTop = tk.Toplevel()
        updateSchoolTop.title('Update School')
        updateSchoolTop.resizable(False,False)
        updateField = []
        updateField.append(tk.StringVar())
        updateField.append(tk.StringVar())
        updateField.append(tk.StringVar())
        updateField.append(tk.StringVar())
        for i in range(len(updateField)):
            updateField[i].set(schoolValues[i])
        updateSchoolTop.columnconfigure(0, weight=1)
        updateSchoolTop.columnconfigure(1, weight=3)
        
        def updateSchoolInfo():
            oldEducation = Entities.Education(employeeId,schoolValues[0],schoolValues[2],schoolValues[3],schoolValues[1])
            neweducation = Entities.Education(employeeId,updateField[0].get(),startDateCalendar.selection_get(),endDateCalendar.selection_get(),updateField[1].get())
            status = Service.updateEducation(oldEducation,neweducation)
            if status == True:
                print("School updated")
                #messagebox.showinfo("School Update", "School updated")
                schoolList.item(selectedSchool,values=(updateField[0].get(),updateField[1].get(),startDateCalendar.selection_get(),endDateCalendar.selection_get()))
                updateSchoolTop.destroy()
            else:
                print(status)
                #messagebox.showinfo("School Update", status)
            
        schoolNameLabel = tk.Label(updateSchoolTop,text='School Name: ')
        schoolNameLabel.grid(row=0,column=0,padx=5,pady=5)
        schoolTypeLabel = tk.Label(updateSchoolTop,text='School Type: ')
        schoolTypeLabel.grid(row=1,column=0,padx=5,pady=5)
        startDateLabel = tk.Label(updateSchoolTop,text='Start Date: ')
        startDateLabel.grid(row=2,column=0,padx=5,pady=5)
        endDateLabel = tk.Label(updateSchoolTop,text='End Date: ')
        endDateLabel.grid(row=3,column=0,padx=5,pady=5)
        updateButton = tk.Button(updateSchoolTop,text="Update", command=updateSchoolInfo)
        updateButton.grid(row=4,column=1,padx=5,pady=5)
        #create entry fields and link them to the variables
      
        schoolNameEntry = tk.Entry(updateSchoolTop,textvariable=updateField[0])
        schoolNameEntry.grid(row=0,column=1,padx=5,pady=5)
        
        comboText = tk.StringVar()
        comboText = updateField[1]
        schoolTypeComboBox = Combobox(updateSchoolTop,values=('High School','Bachelors','Masters'),textvariable=comboText,state='readonly')
        schoolTypeComboBox.grid(row=1,column=1,padx=5,pady=5)
        
        startDateCalendar = Calendar(updateSchoolTop)
        startdatetime = datetime.strptime(str(updateField[2].get()), '%Y-%m-%d')
        
        startDateCalendar.selection_set(startdatetime)
        startDateCalendar.grid(row=2,column=1,padx=5,pady=5)
        
        endDateCalendar = Calendar(updateSchoolTop)
        enddatetime = datetime.strptime(str(updateField[3].get()), '%Y-%m-%d')
 
        endDateCalendar.selection_set(enddatetime)
        endDateCalendar.grid(row=3,column=1,padx=5,pady=5)
        

    addSchoolButton = ttk.Button(scrollable_frame,text='Add',command=addSchoolTopLevel)
    addSchoolButton.grid(row=7,column=0,padx=5,pady=5)
    updateSchoolButton = ttk.Button(scrollable_frame,text='Update',command=updateSchoolTopLevel)
    updateSchoolButton.grid(row=7,column=1,padx=5,pady=5)
    deleteSchoolButton = ttk.Button(scrollable_frame,text='Delete',command=deleteSchool)
    deleteSchoolButton.grid(row=7,column=2,padx=5,pady=5)
        
    
    #--------------------------------------------------
    ttk.Label(scrollable_frame,text="Experience Information",font="Times 30").grid(row=8,column=1,padx=5,pady=5)
    
    experienceColumns = ('Company Name', 'Position', 'Start Date','End Date')
    experienceList = ttk.Treeview(scrollable_frame, columns=experienceColumns, show='headings')

    for col in experienceColumns:
        experienceList.heading(col, text=col)

    experiences = Service.getExperience(employeeId)
    
    for exp in experiences: 
        experienceList.insert('', 'end', text="1", values=(exp.companyName, exp.positionName, exp.startDate, exp.endDate))
    
    experienceList.grid(row=9,padx=5,pady=5,columnspan=3)
    
    scrollbarExperience = ttk.Scrollbar(scrollable_frame, orient=tk.VERTICAL, command=experienceList.yview)
    experienceList.configure(yscrollcommand=scrollbarExperience.set)
    scrollbarExperience.grid(row=9,column=3, sticky='ns',padx=5,pady=5)
    
    def addExperienceTopLevel():
        addExperienceTop = tk.Toplevel()
        addExperienceTop.title('Add Experience')
        addExperienceTop.resizable(False,False)
        
        addExperienceTop.columnconfigure(0, weight=1)
        addExperienceTop.columnconfigure(1, weight=3)
        
        companyNameLabel = tk.Label(addExperienceTop,text='Company Name: ')
        companyNameLabel.grid(row=0,column=0,padx=5,pady=5)
        positionLabel = tk.Label(addExperienceTop,text='Position: ')
        positionLabel.grid(row=1,column=0,padx=5,pady=5)
        startDateLabel = tk.Label(addExperienceTop,text='Start Date: ')
        startDateLabel.grid(row=2,column=0,padx=5,pady=5)
        endDateLabel = tk.Label(addExperienceTop,text='End Date: ')
        endDateLabel.grid(row=3,column=0,padx=5,pady=5)
        
        companyNameEntry = tk.Entry(addExperienceTop)
        companyNameEntry.grid(row=0,column=1,padx=5,pady=5)
        positionEntry = tk.Entry(addExperienceTop)
        positionEntry.grid(row=1,column=1,padx=5,pady=5)
        
        startDateCalendar = Calendar(addExperienceTop)
        startDateCalendar.grid(row=2,column=1,padx=5,pady=5)
        endDateCalendar = Calendar(addExperienceTop)
        endDateCalendar.grid(row=3,column=1,padx=5,pady=5)
        
        def submitExperience():
            newExperience = Entities.Experience(employeeId,startDateCalendar.selection_get(),endDateCalendar.selection_get(),positionEntry.get(),companyNameEntry.get())
            status = Service.addExperience(newExperience)
            if(status == True):
                print("Experience added")
                #messagebox.showinfo("Experience Add", "Experience added")
                experienceList.insert('', 'end',values=(newExperience.companyName,newExperience.positionName,newExperience.startDate,newExperience.endDate))
                addExperienceTop.destroy()
            else:
                print(status)
                #messagebox.showinfo("Experience Add", status)
            
        submitButton = tk.Button(addExperienceTop,text='Submit',command=submitExperience)
        submitButton.grid(row=4,column=1,padx=5,pady=5)
    
    def deleteExperience():
        selectedExperience = experienceList.selection()[0]
        experienceValues = experienceList.item(selectedExperience)['values']
        experience = Entities.Experience(employeeId,experienceValues[2],experienceValues[3],experienceValues[1],experienceValues[0])
        status = Service.deleteExperience(experience)
        if(status == True):
            print("Experience deleted")
            #messagebox.showinfo("Experience Delete", "Experience deleted")
            experienceList.delete(selectedExperience)
        else:
            print(status)
            #messagebox.showinfo("Experience Delete", status)
            
    def updateExperienceTopLevel():
        selectedExperience = experienceList.selection()[0]
        experienceValues = experienceList.item(selectedExperience)['values']
        print(experienceValues)
        updateExperienceTop = tk.Toplevel()
        updateExperienceTop.title('Update Experience')
        updateExperienceTop.resizable(False,False)
        updateField = []
        updateField.append(tk.StringVar())
        updateField.append(tk.StringVar())
        updateField.append(tk.StringVar())
        updateField.append(tk.StringVar())
        for i in range(len(updateField)):
            updateField[i].set(experienceValues[i])
        updateExperienceTop.columnconfigure(0, weight=1)
        updateExperienceTop.columnconfigure(1, weight=3)
        
        def updateExperienceInfo():
            oldExperience = Entities.Experience(employeeId,experienceValues[2],experienceValues[3],experienceValues[1],experienceValues[0])
            newExperience = Entities.Experience(employeeId,startDateCalendar.selection_get(),endDateCalendar.selection_get(),updateField[1].get(),updateField[0].get())
            status = Service.updateExperience(oldExperience,newExperience)
            if status == True:
                print("Experience updated")
                #messagebox.showinfo("Experience Update", "Experience updated")
                experienceList.item(selectedExperience,values=(updateField[0].get(),updateField[1].get(),startDateCalendar.selection_get(),endDateCalendar.selection_get()))
                updateExperienceTop.destroy()
            else:
                print(status)
                #messagebox.showinfo("Experience Update", status)
            
        companyNameLabel = tk.Label(updateExperienceTop,text='Company Name: ')
        companyNameLabel.grid(row=0,column=0,padx=5,pady=5)
        positionLabel = tk.Label(updateExperienceTop,text='Position: ')
        positionLabel.grid(row=1,column=0,padx=5,pady=5)
        startDateLabel = tk.Label(updateExperienceTop,text='Start Date: ')
        startDateLabel.grid(row=2,column=0,padx=5,pady=5)
        endDateLabel = tk.Label(updateExperienceTop,text='End Date: ')
        endDateLabel.grid(row=3,column=0,padx=5,pady=5)
        updateButton = tk.Button(updateExperienceTop,text="Update", command=updateExperienceInfo)
        updateButton.grid(row=4,column=1,padx=5,pady=5)
        #create entry fields and link them to the variables
        companyNameEntry = tk.Entry(updateExperienceTop,textvariable=updateField[0])
        companyNameEntry.grid(row=0,column=1,padx=5,pady=5)
        positionEntry = tk.Entry(updateExperienceTop,textvariable=updateField[1])
        positionEntry.grid(row=1,column=1,padx=5,pady=5)
        
        startDateCalendar = Calendar(updateExperienceTop)
        startdatetime = datetime.strptime(str(updateField[2].get()), '%Y-%m-%d')
        
        startDateCalendar.selection_set(startdatetime)
        startDateCalendar.grid(row=2,column=1,padx=5,pady=5)
        
        endDateCalendar = Calendar(updateExperienceTop)
        enddatetime = datetime.strptime(str(updateField[3].get()), '%Y-%m-%d')
 
        endDateCalendar.selection_set(enddatetime)
        endDateCalendar.grid(row=3,column=1,padx=5,pady=5)
    
    addExperienceButton = ttk.Button(scrollable_frame,text='Add',command=addExperienceTopLevel)
    addExperienceButton.grid(row=10,column=0,padx=5,pady=5)
    updateExperienceButton = ttk.Button(scrollable_frame,text='Update',command=updateExperienceTopLevel)
    updateExperienceButton.grid(row=10,column=1,padx=5,pady=5)
    deleteExperienceButton = ttk.Button(scrollable_frame,text='Delete',command=deleteExperience)
    deleteExperienceButton.grid(row=10,column=2,padx=5,pady=5)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    ttk.Label(scrollable_frame,text="My Applications",font="Times 30").grid(row=11,column=1,padx=5,pady=5)
    
    
    applicationColumns = ('Application Id','Application Name','Company Name', 'Application Date','Counter','Contract Type', 'Position Name','Description','Apply Date','Status')
    applicationListView = ttk.Treeview(scrollable_frame, columns=applicationColumns, show='headings')

    # set column headings
    for col in applicationColumns:
        applicationListView.column(col,minwidth=10,width=100)
        applicationListView.heading(col, text=col)

    status, applicationList = Service.getApplicationView(employeeId)
    if status == True:
        print("Applications retrieved")
        print(applicationList)
        for app in applicationList: 
            applicationListView.insert('', 'end', text="1", values=(app.applicationId , app.applicationName,app.companyName,app.applicationDate, app.counter, app.contractType,app.positionName,app.description,app.appliedApplicationDate,app.status))
    else:   
        print(status)
        #messagebox.showinfo("Applications", status)
        
    applicationListView.grid(row=12,padx=5,pady=5,columnspan=3)
    
    scrollbarApplications = ttk.Scrollbar(scrollable_frame, orient=tk.VERTICAL, command=applicationListView.yview)
    applicationListView.configure(yscrollcommand=scrollbarApplications.set)
    scrollbarApplications.grid(row=12,column=3, sticky='ns',padx=5,pady=5)

    
