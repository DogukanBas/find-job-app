import psycopg2
import Backend.Helper as Helper
from Backend.Entities import *
from psycopg2.errors import *


def registerEmployer(employer,account):
    if(employer.employerName == None or employer.employerSurname) :
        return "Name and Surname cannot be empty."
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

    except(Exception, psycopg2.errors.UniqueViolation) as error:
        print("UniqueViolation")
        return "The username already taken. Please try another one."
    
    except(Exception, psycopg2.errors.NotNullViolation) as error2:
        print("NotNullViolation")
        return "Username and password cannot be empty."    
    
    except(Exception, psycopg2.DatabaseError) as error:
        print("Transaction")
        return ("Unvalid Phone Number. Please try again.")
    
    return True


def registerEmployee(employee,account):
    if(employee.employeeName==None or employee.employeeSurname==None):
        return "Name and Surname cannot be empty."
    ##check password in sql

        
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
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
    except(Exception, psycopg2.errors.UniqueViolation) as error:
        print("UniqueViolation")
        return "The username already taken. Please try another one."
    
    except(Exception, psycopg2.errors.NotNullViolation) as error2:
        print("NotNullViolation")
        return "Username and password cannot be empty."   
    
    except(Exception, psycopg2.DatabaseError) as error:
        print("Transaction")
        return ("Unvalid Phone Number. Please try again.")
    
    return True


def loginCheck(account):
    
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        print(account.userName) 
        print(account.password)
        query = "SELECT * FROM account"
        values = (account.userName, account.password)
        cur.execute(query,values) 
        userType = cur.fetchone()
        print(userType)
        
        if(len(userType) == 0):
            print("No such user")
            return "No such user"
        else:
            if(userType[0][0] == "True"):
                return "Employee"
            else:
                return "Employer"
                
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return error
        

# login(Account(0,"usernaeme","1234","false"))
# registerEmployer(Employer(0,"aktif","1234","bakirkoy"),Account(0,"usernaeme","1234","False"))