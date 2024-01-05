import psycopg2
import Backend.Helper as Helper
from Backend.Entities import *
import Backend.Entities as Entities
from psycopg2.errors import *
from datetime import datetime

Helper.DataBaseConnector.singleton = Helper.DataBaseConnector()

def registerEmployer(employer,account):
    if(employer.employerName == None) :
        return "Name cannot be empty."
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        insertQuery="INSERT INTO account(accountId,username,pass,userType) VALUES(%s,%s,%s,%s)"
        cur.execute("SELECT nextval('accountIdGenerator')")
        accountID= cur.fetchone()[0]
        values=(accountID,account.userName,account.password,account.userType)
        cur.execute(insertQuery,values)
        insertQuery = "UPDATE employer SET employerName = %s, employerPhone = %s, employerAddress = %s WHERE employerId = %s"
        values = (employer.employerName, employer.employerPhone,employer.employerAdress, accountID)
        cur.execute(insertQuery,values)
        conn.commit()

    except( psycopg2.errors.UniqueViolation) as error:
        print("UniqueViolation" + employer.employerName + " " + employer.employerPhone + " " + employer.employerAdress)
        conn.rollback()
        return "The username already taken. Please try another one."
    
    except( psycopg2.errors.NotNullViolation) as error2:
        print("NotNullViolation")
        conn.rollback()
        return "Username and password cannot be empty."    
    
    except( psycopg2.DatabaseError) as error:
        print(error)
        isPassError = str(error).find("check_pass_length")
        print("Transaction")
        conn.rollback()
        if(isPassError != -1):
            return ("Password must be between 6 and 12 characters.")
        return ("Unvalid Phone Number. Please try again.")
    
    except(Exception) as error:
        print(error)
        conn.rollback()
        return "Unknown error"
    
    return True


def registerEmployee(employee,account):
    if (employee.employeeName == None or employee.employeeSurname == None):
        return "Name and Surname cannot be empty."
     
        
    ##check password in sql

    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    # set save point
    try:
        insertQuery="INSERT INTO account(accountId,username,pass,userType) VALUES(%s,%s,%s,%s)"
        cur.execute("SELECT nextval('accountIdGenerator')")
        accountID= cur.fetchone()[0]
        values=(accountID,account.userName,account.password,account.userType)
        cur.execute(insertQuery,values)
        insertQuery = "UPDATE employee SET employeeName = %s, employeeSurname = %s, employeePhone = %s, employeeAddress = %s where employeeId = %s"
        values = (employee.employeeName, employee.employeeSurname,employee.employeePhone,employee.employeeAddress, accountID)
        cur.execute(insertQuery,values)
        conn.commit()
    except(psycopg2.errors.UniqueViolation) as error:
        print("UniqueViolation")
        conn.rollback()
        return "The username already taken. Please try another one."
    
    except( psycopg2.errors.NotNullViolation) as error2:
        print("NotNullViolation")
        conn.rollback()
        return "Username and password cannot be empty."   
    
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        isPassError = str(error).find("check_pass_length")
        print("Transaction")
        conn.rollback()
        if(isPassError != -1):
            return ("Password must be between 6 and 12 characters.")
        return ("Unvalid Phone Number. Please try again.")
    
    return True

def getEmployeeInfo(employeeId):
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        query = "SELECT * FROM employee where employeeId = %s"
        values = (employeeId,)
        cur.execute(query,values) 
        employee = cur.fetchone()
        newEmployee = Entities.Employee(employee[0],employee[1],employee[2],employee[3],employee[4])
        return True,newEmployee
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return False,error

def updateEmployeeInfo(employee):
    if (employee.employeeName == None or employee.employeeSurname == None):
        return "Name and Surname cannot be empty."
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        insertQuery = "UPDATE employee SET employeeName = %s, employeeSurname = %s, employeePhone = %s, employeeAddress = %s where employeeId = %s"
        values = (employee.employeeName, employee.employeeSurname,employee.employeePhone,employee.employeeAddress, employee.employeeId)
        cur.execute(insertQuery,values)
        conn.commit()
        return True
    except(psycopg2.errors.UniqueViolation) as error:
        print("UniqueViolation")
        conn.rollback()
        return "The username already taken. Please try another one."
    
    except( psycopg2.errors.NotNullViolation) as error2:
        print("NotNullViolation")
        conn.rollback()
        return "Username and password cannot be empty."   
    
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("Transaction")
        conn.rollback()
        return ("Unvalid Phone Number. Please try again.")
    
    return True 

def loginCheck(account):
    if(account.userName is None or account.password is None):
        return "Username and password cannot be empty.",None
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    
    try:
        query = "SELECT * from loginCheck(%s,%s)"
        values = (account.userName, account.password)
        cur.execute(query,values) 
        accountInfo = cur.fetchone()
        
        userType,accountId = accountInfo
        if(userType == "No such user"):
            return userType,None
        return userType,accountId
                
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return error
    

def checkExistanceEducation(education): 
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    
    try:
        query = "SELECT checkExistanceEducation(%s,%s,%s,%s,%s)"
        values = (education.employeeId, education.schoolName, education.startDate, education.endDate, education.schoolType)
        cur.execute(query,values) 
        education = cur.fetchone()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        return education[0]
                
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error

    
def addEducation(education):
    if(education.schoolName == None or education.startDate == None or education.schoolType == None):
        return "School name, start date and school type cannot be empty."
    
    if(education.endDate != None and stringToDate(education.endDate) < stringToDate(education.startDate)):
        print(type(education.endDate))
        return "End date cannot be before start date."
    
    if(checkExistanceEducation(education)):
        print("School already exists")
        return "School already exists"
    
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    
    try:
        insertQuery = "INSERT INTO employee_education (employeeid, schoolname, startdate, enddate, schooltype) VALUES (%s, %s, %s, %s, %s)"
        values = (education.employeeId, education.schoolName, education.startDate, education.endDate, education.schoolType)
        cur.execute(insertQuery,values)
        conn.commit()
        return True
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error
    

def updateEducation(oldEducation,newEducation):
    if(oldEducation.schoolName == newEducation.schoolName and stringToDate(oldEducation.startDate).date() == stringToDate(newEducation.startDate) and stringToDate(oldEducation.endDate).date() == stringToDate(newEducation.endDate) and oldEducation.schoolType == newEducation.schoolType):
        return True
   
    if(newEducation.schoolName == None or newEducation.startDate == None or newEducation.schoolType == None):
        return "School name, start date and school type cannot be empty."
    
    if(newEducation.endDate != None and stringToDate(newEducation.endDate) < stringToDate(newEducation.startDate)):
        return "End date cannot be before start date."
    
    if(checkExistanceEducation(newEducation)):
        print("School already exists")
        return "School already exists"
    
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor

    try:
        insertQuery = "UPDATE employee_education SET schoolname = %s, startdate = %s, enddate = %s, schooltype = %s WHERE employeeid = %s and schoolname = %s and startdate = %s and enddate = %s and schooltype = %s"
        values = (newEducation.schoolName, newEducation.startDate, newEducation.endDate, newEducation.schoolType,oldEducation.employeeId, oldEducation.schoolName, oldEducation.startDate,  oldEducation.endDate, oldEducation.schoolType)
        cur.execute(insertQuery,values)
        conn.commit()
        return True
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error


def deleteEducation(education):
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    
    try:
        insertQuery = "DELETE FROM employee_education WHERE employeeid = %s and schoolname = %s and startdate = %s and enddate = %s and schooltype = %s"
        values = (education.employeeId, education.schoolName, education.startDate, education.endDate, education.schoolType)
        cur.execute(insertQuery,values)
        conn.commit()
        return True
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error

def getEducation(employeeId):
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        query = "SELECT * FROM employee_education where employeeid = %s"
        values = (employeeId,)
       
        print(values)
        cur.execute(query,values)
     
        education = cur.fetchall()
        educationList = []
        for edu in education:
            newEducation = Entities.Education(edu[0],edu[1],edu[2],edu[3],edu[4])
            educationList.append(newEducation)
     
        return educationList
                    
    except(Exception, psycopg2.DatabaseError) as error:
       
        print(error)
        conn.rollback()
        return error

def checkExistanceExperience(experience): 
   
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    
    try:
        query = "SELECT checkExistanceExperience(%s,%s,%s,%s,%s)"
        values = (experience.employeeId, experience.startDate, experience.endDate, experience.positionName,experience.companyName)
        cur.execute(query,values) 
        experience = cur.fetchone()
        return experience[0]
                
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error

def addExperience(experience):
    if(experience.companyName == None or experience.startDate == None or experience.positionName == None):
        return "Company name, start date and position cannot be empty."
    
    if(experience.endDate != None and stringToDate(experience.endDate) < stringToDate(experience.startDate)):
        return "End date cannot be before start date."
    
    if(checkExistanceExperience(experience)):
        print("Experience already exists")
        return "Experience already exists"
    
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    
    try:
        insertQuery = "INSERT INTO employee_experience (employeeId, companyName, startDate, endDate, positionName) VALUES (%s, %s, %s, %s, %s)"
        values = (experience.employeeId, experience.companyName, experience.startDate, experience.endDate, experience.positionName)
        cur.execute(insertQuery,values)
        conn.commit()
        return True
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error
    
def updateExperience(oldExperience,newExperience):
    if(newExperience.companyName == None or newExperience.startDate == None or newExperience.positionName == None):
        return "Company name, start date and position cannot be empty."
    
    if(newExperience.endDate != None and stringToDate(newExperience.endDate) < stringToDate(newExperience.startDate)):
        return "End date cannot be before start date."
    
    if(checkExistanceExperience(newExperience)):
        print("Experience already exists")
        return "Experience already exists"
    
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor

    try:
        insertQuery = "UPDATE employee_experience SET companyName = %s, startDate = %s, endDate = %s, positionName = %s WHERE employeeId = %s and companyName = %s and startDate = %s and endDate = %s and positionName = %s"
        values = (newExperience.companyName, newExperience.startDate, newExperience.endDate, newExperience.positionName,oldExperience.employeeId, oldExperience.companyName, oldExperience.startDate, oldExperience.endDate, oldExperience.positionName)
        cur.execute(insertQuery,values)
        conn.commit()
        return True
    
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error
    

def deleteExperience(experience):
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    
    try:
        insertQuery = "DELETE FROM employee_experience WHERE employeeId = %s and companyName = %s and startDate = %s and endDate = %s and positionname = %s"
        values = (experience.employeeId, experience.companyName, experience.startDate, experience.endDate, experience.positionName)
        cur.execute(insertQuery,values)
        conn.commit()
        return True
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error

def getExperience(employeeId):
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    
    try:
        query = "SELECT * FROM employee_experience where employeeId = %s"
        values = (employeeId,)
        cur.execute(query,values) 
        experience = cur.fetchall()
        experiencelist= []
        for exp in experience:
            newExperience = Entities.Experience(exp[0],exp[1],exp[2],exp[3],exp[4])
            experiencelist.append(newExperience)
        return experiencelist
                
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error
    
def stringToDate(date):
    if(type(date)==str):
        datetime_object = datetime.strptime(date, '%Y-%m-%d')
        return datetime_object
    else:
        return date
    
 #EMPLOYER FUNCTIONS

def getEmployerInfo(employerId):
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        query = "SELECT * FROM employer where employerId = %s"
        values = (employerId,)
        cur.execute(query,values) 
        employer = cur.fetchone()
        newEmployer = Entities.Employer(employer[0],employer[1],employer[2],employer[3])
        return True,newEmployer
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return False,error

def updateEmployerInfo(employer):
    if(employer.employerName == None):
        return "Name cannot be empty."
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        insertQuery = "UPDATE employer SET employerName = %s, employerPhone = %s, employerAddress = %s where employerId = %s"
        values = (employer.employerName, employer.employerPhone,employer.employerAdress, employer.employerId)
        cur.execute(insertQuery,values)
        conn.commit()
        return True
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error
    
def getEmployerInfo(employerId):
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        query = "SELECT * FROM employer where employerId = %s"
        values = (employerId,)
        cur.execute(query,values) 
        employer = cur.fetchone()
        newEmployer = Entities.Employer(employer[0],employer[1],employer[2],employer[3])
        return True,newEmployer
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return False,error
    
def getApplications(employerId):
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        query = "SELECT * FROM applications where employerId = %s and isActive = true"
        values = (employerId,)
        cur.execute(query,values) 
        applications = cur.fetchall()
        applicationList = []
        for app in applications:
            newApplication = Entities.Application(app[0],app[1],app[2],app[3],app[4],app[5],app[6],app[7],app[8])
            applicationList.append(newApplication)
        return applicationList
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error

def getApplication(applicationId):
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        query = "SELECT * FROM applications where applicationId = %s and isActive = true"
        values = (applicationId,)
        cur.execute(query,values) 
        application = cur.fetchone()
        newApplication = Entities.Application(application[0],application[1],application[2],application[3],application[4],application[5],application[6],application[7],application[8])
        return newApplication
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error


def addApplication(application):
    if(application.applicationName == None or application.contractType == None or application.positionName == None):
        return False,"Application name, contract type and position cannot be empty."
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    cur.execute("SELECT nextval('advertisementIdGenerator')")
    applicationId= cur.fetchone()[0]

    try:
        insertQuery = "INSERT INTO applications (applicationId, applicationName, applicationDate, contractType, positionName, description, employerId, counter,isactive) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)"
     
        applicationDate= datetime.now().strftime("%Y-%m-%d")
        values = (applicationId,application.applicationName, applicationDate, application.contractType, application.positionName, application.description, application.employerId, 0,True)
        
        cur.execute(insertQuery,values)
        conn.commit()
        return True, Entities.Application(application.employerId,applicationId,0,application.applicationName,applicationDate,application.contractType,application.positionName,application.description,application.isActive)
    
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error
    

#sql fonksiyonuna çevrilecek -------------------->
def deleteApplication(application):
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    applicationId= application.applicationId
    try:
        insertQuery = "select deleteapplication(%s)"
        values = (applicationId,)
        cur.execute(insertQuery,values)
        conn.commit()
        return True
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error
    
def updateApplication(application):
    if(application.applicationName == None or application.applicationDate == None or application.contractType == None or application.positionName == None):
        return "Application name, application date, contract type and position cannot be empty."
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        insertQuery = "UPDATE applications SET applicationName = %s, applicationDate = %s, contractType = %s, positionName = %s, description = %s WHERE applicationId = %s"
        values = (application.applicationName, application.applicationDate, application.contractType, application.positionName, application.description,application.applicationId)
        cur.execute(insertQuery,values)
        conn.commit()
        return True
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error

def showAllApplications(employeeId):
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        query="Select *  from applications where isActive = true and applicationId not in (Select applicationId from appliedapplications where employeeId = " + str(employeeId) + ")"
        cur.execute(query) 
        applications = cur.fetchall()
        applicationList = []
        # query for count of applicants
        query="SELECT COUNT(*) FROM applications WHERE isActive = true and applicationId not in (Select applicationId from appliedapplications where employeeId = " + str(employeeId) + ")"
        cur.execute(query)
        count = cur.fetchone()[0]
        for app in applications:
            newApplication = Entities.Application(app[0],app[1],app[2],app[3],app[4],app[5],app[6],app[7],app[8])
            query="SELECT employername FROM employer where employerId = %s"
            values=(app[0],)

            cur.execute(query,values)
            employerName=cur.fetchone()[0]
            print("employename: ",employerName)    
            applicationList.append((employerName,newApplication))
        return applicationList,count
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error,0


def filterApplications(employeeId,filter):
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    queryCounter = "Select count(*) from ("
    try:
        query="Select * from applications where  isActive = true and applicationId not in (Select applicationId from appliedapplications where employeeId = " + str(employeeId) + ")"
        if(filter.applicationDate != None):
            if(filter.applicationDate == "Ascending"):
                query += " order by applicationDate asc"
            elif(filter.applicationDate == "Descending"):
                query += " order by applicationDate desc"
        
        if(filter.applicationName != None):
            query += " intersect "
            query += "Select * from applications where UPPER(applicationName) like UPPER('%" + filter.applicationName + "%')"

        if(filter.companyName != None):
            query += " intersect "
            query += "Select * from applications where employerId in (Select employerId from employer where employerName like '%" + filter.companyName + "%')"
        
        if(filter.positionName != None):
            query += " intersect "
            query += "Select * from applications where UPPER(positionName) like UPPER('%" + filter.positionName + "%')"
        
        if(filter.contractType != None):
            query += " intersect "
            query += "Select * from applications where UPPER(contractType) like UPPER('%" + filter.contractType + "%')"
        
        queryCounter += query + ")I"
        cur.execute(query)
        applications = cur.fetchall()
        applicationList = []
        # query for count of applicants
        cur.execute(queryCounter)
        count = cur.fetchone()[0]
        for app in applications:
            newApplication = Entities.Application(app[0],app[1],app[2],app[3],app[4],app[5],app[6],app[7],app[8])
            query="SELECT employername FROM employer where employerId = %s"
            values=(app[0],)
            cur.execute(query,values)
            employerName=cur.fetchone()[0]
            applicationList.append((employerName,newApplication))
        return True,applicationList,count 

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return False,error,0
    

def applyApplication(appliedApplication):
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        controlQuery = "select count(*) from appliedapplications where status = 'waiting' and employeeid=%s having count(*) = 3"
        values = (appliedApplication.employeeId,)
        cur.execute(controlQuery,values)
        count = cur.fetchone()
        if(count !=  None):
            return "You have reached the maximum number of waiting applications."
        
        insertQuery = "INSERT INTO appliedapplications (employeeId, applicationId, status, applicationDate,coverLetter) VALUES (%s, %s, %s, %s, %s)"
        applicationDate= datetime.now().strftime("%Y-%m-%d")
        values = (appliedApplication.employeeId, appliedApplication.applicationId, appliedApplication.status, applicationDate, appliedApplication.coverLetter)
        cur.execute(insertQuery,values)
        conn.commit()
        return True
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error


def getApplicationView(employeeId) :
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        query = "SELECT * FROM applicationView where employeeId = %s"
        values = (employeeId,)
        cur.execute(query,values) 
        applications = cur.fetchall()
        applicationList = []
        for app in applications:
            newApplication = Entities.ApplicationView(app[0],app[1],app[2],app[3],app[4],app[5],app[6],app[7],app[8],app[9],app[10],app[11])
            applicationList.append(newApplication)
        return True,applicationList
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return False,error


def getApplicantsView(applicationId):
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        query = "SELECT * FROM applicantsView where applicationId = %s and status = 'waiting'"
        values = (applicationId,)
        cur.execute(query,values) 
        applicants = cur.fetchall()
        applicantList = []
        for app in applicants:
            newApplicant = Entities.ApplicantsView(app[0],app[1],app[2],app[3],app[4],app[5],app[6],app[7],app[8])
            applicantList.append(newApplicant)
        return True,applicantList
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return False,error

def evaluate(applicationId,employeeId,status):
    if(status):
        status = "approved"
    else:
        status = "rejected"
    
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        insertQuery = "UPDATE appliedapplications SET status = %s WHERE applicationId = %s and employeeId = %s"
        values = (status,applicationId,employeeId)
        cur.execute(insertQuery,values)
        conn.commit()
        return True
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error

