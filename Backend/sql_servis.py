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
        print("Transaction")
        print(error)
        conn.rollback()
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
        print(account.userName) 
        print(account.password)
        query = "SELECT userType,accountid FROM account where username = %s and pass = %s"
        values = (account.userName, account.password)
        cur.execute(query,values) 
        accountInfo = cur.fetchone()
        # accountInfo[0] = userType , accountInfo[1] = accountId
        if(accountInfo == None):
            print("No such user")
            return "No such user", None
        
        else:
            if(accountInfo[0] == True):
                return "Employee", accountInfo[1]
            else:
                return "Employer", accountInfo[1]
                
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return error
    

def checkExistanceEducation(education): 
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    
    try:
        query = "SELECT * FROM employee_education where employeeid = %s and schoolname = %s and startdate = %s and enddate = %s and schooltype = %s"
        values = (education.employeeId, education.schoolName, education.startDate, education.endDate, education.schoolType)
        cur.execute(query,values) 
        education = cur.fetchone()
        print(education)
        if(education == None):
            return False
        else:
            return True
                
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error

    
#okul_eslesmesi  : okul adı, isbulan_id,baslangıc yılı, bitis yili, okul tipi(enum)
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
        query = "SELECT * FROM employee_experience where employeeid = %s and companyname = %s and startdate = %s and enddate = %s and position = %s"
        values = (experience.employeeId, experience.companyName, experience.startDate, experience.endDate, experience.position)
        cur.execute(query,values) 
        experience = cur.fetchone()
        
        if(experience == None):
            return False
        else:
            return experience
                
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error

def addExperience(experience):
    if(experience.companyName == None or experience.startDate == None or experience.position == None):
        return "Company name, start date and position cannot be empty."
    
    if(experience.endDate != None and stringToDate(experience.endDate) < stringToDate(experience.startDate)):
        return "End date cannot be before start date."
    
    if(checkExistanceExperience(experience)):
        print("Experience already exists")
        return "Experience already exists"
    
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    
    try:
        insertQuery = "INSERT INTO employee_experience (employeeId, companyName, startDate, endDate, position) VALUES (%s, %s, %s, %s, %s)"
        values = (experience.employeeId, experience.companyName, experience.startDate, experience.endDate, experience.position)
        cur.execute(insertQuery,values)
        conn.commit()
        return True
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error
    
def updateExperience(oldExperience,newExperience):
    if(newExperience.companyName == None or newExperience.startDate == None or newExperience.position == None):
        return "Company name, start date and position cannot be empty."
    
    if(newExperience.endDate != None and stringToDate(newExperience.endDate) < stringToDate(newExperience.startDate)):
        return "End date cannot be before start date."
    
    if(checkExistanceExperience(newExperience)):
        print("Experience already exists")
        return "Experience already exists"
    
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor

    try:
        insertQuery = "UPDATE employee_experience SET companyName = %s, startDate = %s, endDate = %s, position = %s WHERE employeeId = %s and companyName = %s and startDate = %s and endDate = %s and position = %s"
        values = (newExperience.companyName, newExperience.startDate, newExperience.endDate, newExperience.position,oldExperience.employeeId, oldExperience.companyName, oldExperience.startDate, oldExperience.endDate, oldExperience.position)
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
        insertQuery = "DELETE FROM employee_experience WHERE employeeId = %s and companyName = %s and startDate = %s and endDate = %s and position = %s"
        values = (experience.employeeId, experience.companyName, experience.startDate, experience.endDate, experience.position)
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
        return experience
                
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
    
 