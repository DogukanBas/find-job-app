import tkinter as tk
from tkinter import ttk

def showPage():
    root = tk.Tk() 
    root.title("Main Page") 
    tabControl = ttk.Notebook(root) 
    
    tab1 = ttk.Frame(tabControl) 
    tab2 = ttk.Frame(tabControl) 
    
    tabControl.add(tab1, text ='Advertisements') 
    tabControl.add(tab2, text ='Profile') 
    tabControl.pack(expand = 1, fill ="both") 
    
    ttk.Label(tab1, text ="Welcome to \ GeeksForGeeks").grid(column = 0,  row = 0, padx = 30, pady = 30)   
    
    
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
    
    schoolColumns = ('School Name', 'School Type', 'Start Date','End Date')
    schoolList = ttk.Treeview(tab2, columns=schoolColumns, show='headings')

    # set column headings
    for col in schoolColumns:
        schoolList.heading(col, text=col)

    # Insert the data in Treeview widget
    schoolList.grid(row=5,padx=5,pady=5,columnspan=3)
    
    scrollbarSchool = ttk.Scrollbar(tab2, orient=tk.VERTICAL, command=schoolList.yview)
    schoolList.configure(yscrollcommand=scrollbarSchool.set)
    scrollbarSchool.grid(row=5,column=3, sticky='ns',padx=5,pady=5)
    
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
        schoolTypeEntry = tk.Entry(addSchoolTop)
        schoolTypeEntry.grid(row=1,column=1,padx=5,pady=5)
        startDateEntry = tk.Entry(addSchoolTop)
        startDateEntry.grid(row=2,column=1,padx=5,pady=5)
        endDateEntry = tk.Entry(addSchoolTop)
        endDateEntry.grid(row=3,column=1,padx=5,pady=5)
        
        def submitSchool():
            print(schoolNameEntry.get())
            print(schoolTypeEntry.get())
            print(startDateEntry.get())
            print(endDateEntry.get())
            schoolList.insert('','end',values=(schoolNameEntry.get(),schoolTypeEntry.get(),startDateEntry.get(),endDateEntry.get()))
            addSchoolTop.destroy()
            
        submitButton = tk.Button(addSchoolTop,text='Submit',command=submitSchool)
        submitButton.grid(row=4,column=1,padx=5,pady=5)
        
    def deleteSchool():
        selectedSchool = schoolList.selection()[0]
        schoolList.delete(selectedSchool)

    addSchoolButton = ttk.Button(tab2,text='Add',command=addSchoolTopLevel)
    addSchoolButton.grid(row=6,column=0,padx=5,pady=5)
    updateSchoolButton = ttk.Button(tab2,text='Update')
    updateSchoolButton.grid(row=6,column=1,padx=5,pady=5)
    deleteSchoolButton = ttk.Button(tab2,text='Delete',command=deleteSchool)
    deleteSchoolButton.grid(row=6,column=2,padx=5,pady=5)
        
    
    #--------------------------------------------------
    
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
    experienceList.grid(row=7,padx=5,pady=5,columnspan=3)
    
    scrollbarExperience = ttk.Scrollbar(tab2, orient=tk.VERTICAL, command=experienceList.yview)
    experienceList.configure(yscrollcommand=scrollbarExperience.set)
    scrollbarExperience.grid(row=7,column=3, sticky='ns',padx=5,pady=5)
    
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
    
    addExperienceButton = ttk.Button(tab2,text='Add',command=addExperienceTopLevel)
    addExperienceButton.grid(row=8,column=0,padx=5,pady=5)
    updateExperienceButton = ttk.Button(tab2,text='Update')
    updateExperienceButton.grid(row=8,column=1,padx=5,pady=5)
    deleteExperienceButton = ttk.Button(tab2,text='Delete',command=deleteExperience)
    deleteExperienceButton.grid(row=8,column=2,padx=5,pady=5)
    
    root.mainloop() 