import tkinter as tk
from tkinter import ttk
from Backend import sql_servis as Service
from Backend import Entities
from tkinter import messagebox
from tkinter.ttk import Combobox
#import ttkbootstrap as tb
from tkcalendar import Calendar

def showPage(tab2,employeeId):
    ttk.Label(tab2, text ="Name:").grid(column = 0,  row = 0, padx = 5, pady = 5) 
    ttk.Label(tab2, text ="Surname:").grid(column = 0,  row = 1, padx = 5, pady = 5) 
    ttk.Label(tab2, text ="Address:").grid(column = 0,  row = 2, padx = 5, pady = 5) 
    ttk.Label(tab2, text ="Phone:").grid(column = 0,  row = 3, padx = 5, pady = 5) 
    
    nameEntry = ttk.Entry(tab2)
    nameEntry.grid(row=0,column=1,padx=5,pady=5)
    surnameEntry = ttk.Entry(tab2)
    surnameEntry.grid(row=1,column=1,padx=5,pady=5)
    addressEntry = ttk.Entry(tab2)
    addressEntry.grid(row=2,column=1,padx=5,pady=5)
    phoneEntry = ttk.Entry(tab2)
    phoneEntry.grid(row=3,column=1,padx=5,pady=5)
    
    def saveInfos():
        print(nameEntry.get())
        print(surnameEntry.get())
        print(addressEntry.get())
        print(phoneEntry.get())
    
    saveButton = ttk.Button(tab2,text='Save',command=saveInfos)
    saveButton.grid(row=4,column=1,padx=5,pady=5)
    
    #list past experiences in multi column list
    
    ttk.Label(tab2,text="School Past",font="Times 30").grid(row=5,column=1,padx=5,pady=5)
    
    schoolColumns = ('School Name', 'School Type', 'Start Date','End Date')
    schoolList = ttk.Treeview(tab2, columns=schoolColumns, show='headings')

    # set column headings
    for col in schoolColumns:
        schoolList.heading(col, text=col)

    schoolList.insert('', 'end', text="1", values=('Bosch', 'intern', '2023','2023'))
    schoolList.insert('', 'end', text="1", values=('Bosch', 'intern', '2023','2023'))
    # Insert the data in Treeview widget
    schoolList.grid(row=6,padx=5,pady=5,columnspan=3)
    
    scrollbarSchool = ttk.Scrollbar(tab2, orient=tk.VERTICAL, command=schoolList.yview)
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
        schoolTypeComboBox = Combobox(addSchoolTop,values=('High School','Bachelors','Masters'),textvariable=comboText)
        schoolTypeComboBox.grid(row=1,column=1,padx=5,pady=5)
        startDateCalendar = Calendar(addSchoolTop)
        startDateCalendar.grid(row=2,column=1,padx=5,pady=5)
        endDateCalendar = Calendar(addSchoolTop)
        endDateCalendar.grid(row=3,column=1,padx=5,pady=5)
        # startDateCalendar = tb.DateEntry(addSchoolTop,bootstyle='danger')
        # startDateCalendar.grid(row=2,column=1,padx=5,pady=5)
        # endDateCalendar = tb.DateEntry(addSchoolTop,bootstyle='danger')
        # endDateCalendar.grid(row=3,column=1,padx=5,pady=5)
        
        def submitSchool():
            print(startDateCalendar.get_date())
            print(endDateCalendar.get_date())

            newEducation = Entities.Education(employeeId,schoolNameEntry.get(),startDateCalendar.get_date(),endDateCalendar.get_date(),comboText.get())
            status = Service.addEducation(newEducation)
            if(status == True):
                print("School added")
                messagebox.showinfo("School Add", "School added")
                schoolList.insert('','end',values=(schoolNameEntry.get(),comboText.get(),startDateCalendar.get_date(),endDateCalendar.get_date()))
                addSchoolTop.destroy()
            else: 
                print(status)
                messagebox.showinfo("School Add", status)
                
            
        submitButton = tk.Button(addSchoolTop,text='Submit',command=submitSchool)
        submitButton.grid(row=4,column=1,padx=5,pady=5)
        
    def deleteSchool():
        selectedSchool = schoolList.selection()[0]
        schoolList.delete(selectedSchool)
    
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
            schoolList.item(selectedSchool,values=(updateField[0].get(),updateField[1].get(),updateField[2].get(),updateField[3].get()))
            updateSchoolTop.destroy()
            
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
        schoolTypeEntry = tk.Entry(updateSchoolTop,textvariable=updateField[1])
        schoolTypeEntry.grid(row=1,column=1,padx=5,pady=5)
        startDateCalendar = Calendar(updateSchoolTop)
        startDateCalendar.grid(row=2,column=1,padx=5,pady=5)
        endDateCalendar = Calendar(updateSchoolTop)
        endDateCalendar.grid(row=3,column=1,padx=5,pady=5)
        

    addSchoolButton = ttk.Button(tab2,text='Add',command=addSchoolTopLevel)
    addSchoolButton.grid(row=7,column=0,padx=5,pady=5)
    updateSchoolButton = ttk.Button(tab2,text='Update',command=updateSchoolTopLevel)
    updateSchoolButton.grid(row=7,column=1,padx=5,pady=5)
    deleteSchoolButton = ttk.Button(tab2,text='Delete',command=deleteSchool)
    deleteSchoolButton.grid(row=7,column=2,padx=5,pady=5)
        
    
    #--------------------------------------------------
    ttk.Label(tab2,text="Experience Past",font="Times 30").grid(row=8,column=1,padx=5,pady=5)
    
    experienceColumns = ('Company Name', 'Position', 'Start Date','End Date')
    experienceList = ttk.Treeview(tab2, columns=experienceColumns, show='headings')

    # set column headings
    for col in experienceColumns:
        experienceList.heading(col, text=col)

    # Insert the data in Treeview widget
    experienceList.insert('', 'end', text="1", values=('Bosch', 'intern', '2023','2023'))
    experienceList.insert('', 'end', text="1", values=('Bosch', 'intern', '2023','2023'))
    experienceList.insert('', 'end', text="1", values=('Bosch', 'intern', '2023','2023'))
    experienceList.insert('', 'end', text="1", values=('Bosch', 'intern', '2023','2023'))
    experienceList.insert('', 'end', text="1", values=('Bosch', 'intern', '2023','2023'))
    experienceList.insert('', 'end', text="1", values=('Bosch', 'intern', '2023','2023'))
    experienceList.insert('', 'end', text="1", values=('Bosch', 'intern', '2023','2023'))
    experienceList.insert('', 'end', text="1", values=('Bosch', 'intern', '2023','2023'))
    experienceList.insert('', 'end', text="1", values=('Bosch', 'intern', '2023','2023'))
    experienceList.insert('', 'end', text="1", values=('Bosch', 'intern', '2023','2023'))
    experienceList.insert('', 'end', text="1", values=('Bosch', 'intern', '2023','2023'))
    experienceList.insert('', 'end', text="1", values=('Bosch', 'intern', '2023','2023'))
    experienceList.insert('', 'end', text="1", values=('Bosch', 'intern', '2023','2023'))
    experienceList.insert('', 'end', text="1", values=('Bosch', 'intern', '2023','2023'))
    experienceList.insert('', 'end', text="1", values=('Bosch', 'intern', '2023','2023'))
    experienceList.insert('', 'end', text="1", values=('Bosch', 'intern', '2023','2023'))
    experienceList.grid(row=9,padx=5,pady=5,columnspan=3)
    
    scrollbarExperience = ttk.Scrollbar(tab2, orient=tk.VERTICAL, command=experienceList.yview)
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
        startDateEntry = tk.Entry(addExperienceTop)
        startDateEntry.grid(row=2,column=1,padx=5,pady=5)
        endDateEntry = tk.Entry(addExperienceTop)
        endDateEntry.grid(row=3,column=1,padx=5,pady=5)
        
        def submitExperience():
            print(companyNameEntry.get())
            print(positionEntry.get())
            print(startDateEntry.get())
            print(endDateEntry.get())
            schoolList.insert('','end',values=(companyNameEntry.get(),positionEntry.get(),startDateEntry.get(),endDateEntry.get()))
            addExperienceTop.destroy()
            
        submitButton = tk.Button(addExperienceTop,text='Submit',command=submitExperience)
        submitButton.grid(row=4,column=1,padx=5,pady=5)
    
    def deleteExperience():
        selectedExperience = experienceList.selection()[0]
        experienceList.delete(selectedExperience)
        
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
            experienceList.item(selectedExperience,values=(updateField[0].get(),updateField[1].get(),updateField[2].get(),updateField[3].get()))
            updateExperienceTop.destroy()
            
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
        startDateEntry = tk.Entry(updateExperienceTop,textvariable=updateField[2])
        startDateEntry.grid(row=2,column=1,padx=5,pady=5)
        endDateEntry = tk.Entry(updateExperienceTop,textvariable=updateField[3])
        endDateEntry.grid(row=3,column=1,padx=5,pady=5)
    
    addExperienceButton = ttk.Button(tab2,text='Add',command=addExperienceTopLevel)
    addExperienceButton.grid(row=10,column=0,padx=5,pady=5)
    updateExperienceButton = ttk.Button(tab2,text='Update',command=updateExperienceTopLevel)
    updateExperienceButton.grid(row=10,column=1,padx=5,pady=5)
    deleteExperienceButton = ttk.Button(tab2,text='Delete',command=deleteExperience)
    deleteExperienceButton.grid(row=10,column=2,padx=5,pady=5)
    
    # advertisementColumns = ('Advertisement Name', 'Advertisement Date', 'Contract Type','Position Name','Description','Counter','Application Date','Status')
    # advertisementList = ttk.Treeview(tab2, columns=advertisementColumns, show='headings')

    # # set column headings
    # for col in advertisementColumns:
    #     schoolList.heading(col, text=col)

    # #insert random values
    # advertisementList.insert('', 'end', text="1", values=('Bosch', '2023', 'intern','software','işe alım', '10', '2023','waiting'))

    # # Insert the data in Treeview widget
    # schoolList.grid(row=11,padx=5,pady=5,columnspan=3)
    
    # scrollbarAdvertisement = ttk.Scrollbar(tab2, orient=tk.VERTICAL, command=advertisementList.yview)
    # advertisementList.configure(yscrollcommand=scrollbarAdvertisement.set)
    # scrollbarAdvertisement.grid(row=11,column=3, sticky='ns',padx=5,pady=5)
    
