import tkinter as tk
from tkinter import ttk
from Backend import sql_servis as Service
from Backend import Entities

def showPage(tab1,employeeId):
    
    ttk.Label(tab1, text ="By Date").grid(column = 0,  row = 0, padx = 5, pady = 5)
    ttk.Label(tab1, text ="Application Name").grid(column = 1,  row = 0, padx = 5, pady = 5)
    ttk.Label(tab1, text ="Company Name").grid(column = 2,  row = 0, padx = 5, pady = 5)
    ttk.Label(tab1, text ="Position Name").grid(column = 3,  row = 0, padx = 5, pady = 5)
    ttk.Label(tab1, text ="Contract Type").grid(column = 4,  row = 0, padx = 5, pady = 5)   
 
    dateComboBox = ttk.Combobox(tab1,values=('No Filter','Ascending','Descending'),state='readonly',width=10)
    dateComboBox.set("No Filter")
    dateComboBox.grid(row=1,column=0,padx=5,pady=5)
    
    applicationNameEntry = tk.Entry(tab1,width=10)
    applicationNameEntry.grid(row=1,column=1,padx=5,pady=5)
    
    companyNameEntry = tk.Entry(tab1,width=10)
    companyNameEntry.grid(row=1,column=2,padx=5,pady=5)
    
    positionNameEntry = tk.Entry(tab1,width=10)
    positionNameEntry.grid(row=1,column=3,padx=5,pady=5)
    
    contractTypeComboBox = ttk.Combobox(tab1,values=('No Filter','Full Time','Part Time','Intern'),state='readonly',width=10)
    contractTypeComboBox.set('No Filter')
    contractTypeComboBox.grid(row=1,column=4,padx=5,pady=5)
    
    def filter():
        filter = Entities.Filter(dateComboBox.get(),applicationNameEntry.get(),companyNameEntry.get(),positionNameEntry.get(),contractTypeComboBox.get())
        status, filteredApplications = Service.filterApplications(employeeId,filter)
        if status == True:
            print("Applications filtered")
            applicationListView.delete(*applicationListView.get_children())
            for app in filteredApplications:
                applicationListView.insert('', 'end', text="1", values=(app[1].applicationId , app[1].applicationName,app[0],app[1].applicationDate, app[1].counter, app[1].contractType,app[1].positionName,app[1].description))
        else:
            print("Applications not filtered")
            #messagebox.showerror("Filter", f"Applications not filtered - {status}")
    
    filterButton = tk.Button(tab1,text='Filter',command=filter)
    filterButton.grid(row=2,column=2,padx=5,pady=5)
    
    applicationColumns = ('Application Id','Application Name','Company Name', 'Application Date','Counter','Contract Type', 'Position Name','Description')
    applicationListView = ttk.Treeview(tab1, columns=applicationColumns, show='headings')

    # set column headings
    for col in applicationColumns:
        applicationListView.column(col,minwidth=10,width=100)
        applicationListView.heading(col, text=col)

    applicationList = Service.showAllApplications(employeeId)
    print(applicationList)
    for app in applicationList: 
        applicationListView.insert('', 'end', text="1", values=(app[1].applicationId , app[1].applicationName,app[0],app[1].applicationDate, app[1].counter, app[1].contractType,app[1].positionName,app[1].description))
        
    applicationListView.grid(row=3,padx=5,pady=5,columnspan=5)
    
    scrollbarApplications = ttk.Scrollbar(tab1, orient=tk.VERTICAL, command=applicationListView.yview)
    applicationListView.configure(yscrollcommand=scrollbarApplications.set)
    scrollbarApplications.grid(row=3,column=5, sticky='ns',padx=5,pady=5)
    
    def apply():
        selectedApplication = applicationListView.item(applicationListView.selection()[0])['values']
        coverLetterTopLevel = tk.Toplevel(tab1)
        coverLetterTopLevel.title('Cover Letter')
        coverLetterTopLevel.resizable(False,False)
        coverLabel = tk.Label(coverLetterTopLevel,text="Cover Letter")
        coverLabel.grid(row=0,column=0,padx=5,pady=5)
        coverLetterEntry = tk.Text(coverLetterTopLevel)
        coverLetterEntry.grid(row=1,column=0,padx=5,pady=5)
        
        def send():
            coverLetter = coverLetterEntry.get("1.0",tk.END)
            if(selectedApplication == ""):
                print("No application selected")
                return
            else:
                print(selectedApplication)
                appliedApplication = Entities.AppliedApplications(employeeId,selectedApplication[0],'waiting',None,coverLetter)
                status = Service.applyApplication(appliedApplication)
                if(status == True):
                    print("Application successful")
                    applicationListView.delete(applicationListView.selection()[0])
                    coverLetterTopLevel.destroy()
                    #messagebox.showinfo("Apply", "Application successful")
                else:
                    print("Application failed")
                    #messagebox.showerror("Apply", f"Application failed - {status}")
                    
        sendButton = tk.Button(coverLetterTopLevel,text="Send",command=send)
        sendButton.grid(row=2,column=0,padx=5,pady=5)
    
    applyButton = tk.Button(tab1,text='Apply',command=apply)
    applyButton.grid(row=6,column=2,padx=5,pady=5)
    
    
    
    
    
    