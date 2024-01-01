import psycopg2
import Backend.Helper as Helper
from Backend.Entities import *
from psycopg2.errors import *


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
        return "Username and password cannot be empty."
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
        
        if(education == None):
            return False
        else:
            return education
                
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
        return error

    
#okul_eslesmesi  : okul adı, isbulan_id,baslangıc yılı, bitis yili, okul tipi(enum)
def addEducation(education):
    if(education.schoolName == None or education.startDate == None or education.schoolType == None):
        return "School name, start date and school type cannot be empty."
    
    if(education.endDate != None and education.endDate < education.startDate): 
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
    if(newEducation.schoolName == None or newEducation.startDate == None or newEducation.schoolType == None):
        return "School name, start date and school type cannot be empty."
    
    if(newEducation.endDate != None and newEducation.endDate < newEducation.startDate):
        return "End date cannot be before start date."
    
    if(checkExistanceEducation(newEducation)):
        print("School already exists")
        return "School already exists"
    
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor

    try:
        insertQuery = "UPDATE employee_education SET schoolname = %s, startdate = %s, enddate = %s, schooltype = %s WHERE employeeid = %s and schoolname = %s and startdate = %s and enddate = %s and schooltype = %s"
        values = (newEducation.schoolName, newEducation.startDate, newEducation.endDate, newEducation.schoolType,oldEducation.employeeId, oldEducation.schoolName, oldEducation.startDate, oldEducation.endDate, oldEducation.schoolType)
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